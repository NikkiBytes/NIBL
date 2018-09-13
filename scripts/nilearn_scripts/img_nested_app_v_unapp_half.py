#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:56:59 2018

@author: jennygilbert

"""
#this imports all the commands needed for the script to work#
import os
import numpy as np
import nilearn
import glob
#import matplotlib
import nibabel as nib
from nilearn.image import concat_imgs, index_img, smooth_img
from nilearn.image import resample_to_img
from nilearn import plotting
from nilearn.input_data import NiftiMasker
from sklearn.svm import SVC
from sklearn.cross_validation import LeaveOneLabelOut, cross_val_score, permutation_test_score
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from nilearn import image
#from nilearn.plotting import plot_stat_map, show
from sklearn.dummy import DummyClassifier

#Nested decoding of subjects from the chocolate study
#Decoding of response to app vs. unapp images using an ANOVA-based feature selection, within the power atlas

# ---STEP 1---
#Cncatenate the imagine data into a NIFTI-2 file.
#Note: the data does not fit into a NIFTI-1 file, due to large number of subs.

#set basepath
basepath=os.path.join('/projects','niblab','data','eric_data','W1','imagine')

#make a list of the files to concat
all_func = glob.glob(os.path.join(basepath,'level1_grace_edit','cs*++.feat','filtered_func_data.nii.gz'))
half_func = all_func[:67]
#load in all the files from the glob above, then convert them from nifti1 to nifti2
ni2_funcs = (nib.Nifti2Image.from_image(nib.load(func)) for func in half_func)
#concat, this is with nibabel, but should work with nilearn too
ni2_concat = nib.concat_images(ni2_funcs, check_affines=False, axis=3)
#set the output file name
outfile=os.path.join(basepath,'concatenated_imagine.nii')
#write the file
ni2_concat.to_filename(outfile)

# ---STEP 2---
#load & prepare MRI data
#load, fxnl, anatomical, & mask for plotting
fmri_subjs=os.path.join(basepath, 'concatenated_imagine.nii')
average_ana=os.path.join(basepath,'CS_avg_mprage_image.nii.gz')
imag_mask=os.path.join('/projects','niblab','scripts','nilean_stuff','power_roimask_4bi.nii.gz')

#plot mask (Power ROIs) over anatomical that is defined above
#plotting.plot_roi(imag_mask,bg_img=average_ana,cmap='Paired')

#load labels for the functional data
stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_all_sub.csv')
labels = np.recfromcsv(stim, delimiter=",")
print(labels)
#Its shape corresponds to the number of time-points times the number of voxels in the mask

#Retrieve the behavioral targets, that we are going to predict in the decoding
y_mask = labels['label']
subs = labels['sub']

# ---STEP 3---
#feature selection
#To keep only data corresponding to app food or unapp food, we create a mask of the samples belonging to the condition.
condition_mask = np.logical_or(y_mask == b'app',y_mask == b'unapp')
print(condition_mask.shape)
y = y_mask[condition_mask]
print(y)
n_conditions = np.size(np.unique(y))

#prepare the fxnl data.
nifti_masker = NiftiMasker(mask_img=imag_mask,
                           smoothing_fwhm=4,standardize=True,
                           memory="nilearn_cache",memory_level=1)

fmri_trans = nifti_masker.fit_transform(fmri_subjs)
print(fmri_trans)
X = fmri_trans[condition_mask]
subs = subs[condition_mask]


# ---STEP 4---
#setting prediction  & testing the classifer
svc = SVC(kernel='linear')
print(svc)

# Define the dimension reduction to be used.
# Here we use a classical univariate feature selection based on F-test, namely Anova. We set the number of features to be selected to 500
feature_selection = SelectKBest(f_classif, k=3000)

# We have our classifier (SVC), our feature selection (SelectKBest), and now, we can plug them together in a *pipeline* that performs the two operations successively:
anova_svc = Pipeline([('anova',feature_selection), ('svc',svc)])

#fit the decoder and predict
anova_svc.fit(X, y)
y_pred = anova_svc.predict(X)

cv = LeaveOneLabelOut(subs[subs < 1])

k_range = [10, 15, 30, 50, 150, 300, 500, 1000, 1500, 3000, 5000]
cv_scores = []
scores_validation = []

# we are working with a composite estimator:
# a pipeline of feature selection followed by SVC. Thus to give the name of the parameter that we want to tune we need to give the name of the step in
# the pipeline, followed by the name of the parameter, with ‘__’ as a separator.
# We are going to tune the parameter 'k' of the step called 'anova' in the pipeline. Thus we need to address it as 'anova__k'.
# Note that GridSearchCV takes an n_jobs argument that can make it go much faster
grid = GridSearchCV(anova_svc, param_grid={'anova__k': k_range},n_jobs=-1)
nested_cv_scores = cross_val_score(grid, X, y)
classification_accuracy = np.mean(nested_cv_scores)
print("Classification accuracy: %.4f / Chance level: %f" %
      (classification_accuracy, 1. / n_conditions))

for k in k_range:
    feature_selection.k = k
    cv_scores.append(np.mean(
    cross_val_score(anova_svc, X[subs == 1], y[subs == 1])))
    print("CV score: %.4f" % cv_scores[-1])

    anova_svc.fit(X[subs == 1], y[subs == 1])
    y_pred = anova_svc.predict(X[subs == 0])
    scores_validation.append(np.mean(y_pred == y[subs == 0]))
    print("score validation: %.4f" % scores_validation[-1])


# ---STEP 5---
#flipping the martix backinto an image
coef = svc.coef_
print(coef)

# reverse feature selection
coef = feature_selection.inverse_transform(coef)

# reverse masking
weight_img = nifti_masker.inverse_transform(coef)
#plot image
#plot_stat_map(weight_img, average_ana, title='SVM weights')


# ---STEP 6---
#permunation testing to measure probablility of chance first score is mean accuracy of the null scores without perm targets, then the array, then the p-value.
#null_cv_scores = permutation_test_score(svc, X, y, cv=10)
#print(null_cv_scores)

#from sklearn.dummy import DummyClassifier
null_cv_scoresdumb = cross_val_score(DummyClassifier(), X, y, cv=10)
print(null_cv_scoresdumb)
meannull_cv_scoresdumb = np.mean(null_cv_scoresdumb)
print(meannull_cv_scoresdumb)
