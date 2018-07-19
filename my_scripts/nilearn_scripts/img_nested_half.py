
# coding: utf-8

# In[3]:


import os
import numpy as np
import nilearn
import glob
#import matplotlib
import nibabel as nib
from nilearn.image import concat_imgs, index_img, smooth_img
from nilearn.image import resample_to_img
#from nilearn import plotting
from nilearn.input_data import NiftiMasker
from sklearn.svm import SVC
from sklearn.model_selection import LeaveOneOut, cross_val_score, permutation_test_score
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from nilearn import image
#from nilearn.plotting import plot_stat_map, show
from sklearn.dummy import DummyClassifier
import pandas as pd
from sklearn.cross_validation import LeaveOneLabelOut

# In[4]:


# ---STEP 1---
#Cncatenate the imagine data into a NIFTI-2 file.
#Note: the data does not fit into a NIFTI-1 file, due to large number of subs.

#set basepath
basepath=os.path.join('/projects','niblab','data','eric_data','W1','imagine')
outpath = "/projects/niblab/nilearn_projects"
#make a list of the files to concat
all_func = glob.glob(os.path.join(basepath,'level1_grace_edit','cs*++.feat','filtered_func_data.nii.gz'))
half_func = all_func[:67]


# In[18]:



# ---STEP 2---
#load & prepare MRI data
#load, fxnl, anatomical, & mask for plotting
fmri_subjs=os.path.join(basepath, 'concatenated_imagine.nii')
average_ana=os.path.join(basepath,'CS_avg_mprage_image.nii.gz')
imag_mask=os.path.join(outpath,'power_roimask_4bi.nii.gz')

#plot mask (Power ROIs) over anatomical that is defined above
#plotting.plot_roi(imag_mask,bg_img=average_ana,cmap='Paired')

#load labels for the functional data
stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_67_sub.csv')
labels = np.recfromcsv(stim, delimiter=",",encoding='UTF-8')
#print(labels)
#Its shape corresponds to the number of time-points times the number of voxels in the mask
func_df = pd.read_csv(stim, sep=",")
#Retrieve the behavioral targets, that we are going to predict in the decoding
#y_mask = labels['labels']
#subs = labels['subs']
y_mask =  func_df['labels']
subs = func_df['subs']


# In[19]:



# ---STEP 3---
#feature selection
#To keep only data corresponding to app food or unapp food, we create a mask of the samples belonging to the condition.
#condition_mask = np.logical_or(y_mask == b'app',y_mask == b'unapp')
condition_mask = func_df["labels"].isin(['app', 'unapp'])
print(condition_mask.shape)
#y = y_mask[condition_mask]
y = y_mask[condition_mask]
print(y.shape)

n_conditions = np.size(np.unique(y))
print(n_conditions)
#n_conditions = np.size(np.unique(y))
print(y.unique())
#session = func_df[condition_mask].to_records(index=False)
#print(session.dtype.name)


# In[22]:


#prepare the fxnl data.
nifti_masker = NiftiMasker(mask_img=imag_mask,
                           smoothing_fwhm=4,standardize=True,
                           memory_level=0)

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
k_range = [10, 15, 30, 50 , 150, 300, 500, 1000, 1500, 3000, 5000]
cv_scores = cross_val_score(anova_svc, X[subs ==1], y[subs ==1])

scores_validation = []
cv_means =[]

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
    curr_k = k
    anova_svc.set_params(anova__k=curr_k, svc__C=1).fit(X[subs == 1], y[subs == 1])
    cv_scores = cross_val_score(anova_svc, X[subs ==1], y[subs ==1])
    cv_means.append(cv_scores.mean())
    print("CV score: %.4f" % cv_scores[-1])
    y_pred = anova_svc.predict(X[subs == 0])
    scores_validation.append(cv_scores.mean(y_pred == y[subs == 0]))
    print("score validation: %.4f" % scores_validation[-1])
