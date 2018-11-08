/Users/nikkibytes/Documents/testing/ChocoDataimport matplotlib.pyplot as plt
import os
import numpy as np
import nilearn
import glob
import nibabel as nib
import pandas as pd
from nilearn.image import concat_imgs, index_img, smooth_img
from nilearn.image import resample_to_img
#from nilearn import plotting
from nilearn.input_data import NiftiMasker
from sklearn.svm import SVC
from sklearn.cross_validation import LeaveOneLabelOut
from sklearn.model_selection import  cross_val_score, permutation_test_score
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from nilearn import image
from nilearn.plotting import plot_stat_map, show
from sklearn.dummy import DummyClassifier


#set basepath
basepath=os.path.join('/projects','niblab','data','eric_data','W1','imagine')
outpath = "/projects/niblab/nilearn_projects"
#make a list of the files to concat
all_func = glob.glob(os.path.join(basepath,'level1_grace_edit','cs*++.feat','filtered_func_data.nii.gz'))
half_func = all_func[:67]


# ---STEP 2---
#load & prepare MRI data
#load, fxnl, anatomical, & mask for plotting
fmri_subjs=os.path.join(outpath, 'concatenated_imagine_67.nii')
average_ana=os.path.join(outpath,'CS_avg_mprage_image.nii.gz')
imag_mask=os.path.join(outpath,'power_roimask_4bi.nii.gz')

#plot mask (Power ROIs) over anatomical that is defined above
#plotting.plot_roi(imag_mask,bg_img=average_ana,cmap='Paired')

#load labels for the functional data
stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_67_sub.csv')
#labels = np.recfromcsv(stim, delimiter=",",encoding='UTF-8')
#print(labels)
#Its shape corresponds to the number of time-points times the number of voxels in the mask
func_df = pd.read_csv(stim, sep=",")
#Retrieve the behavioral targets, that we are going to predict in the decoding
#y_mask = labels['labels']
#subs = labels['subs']
y_mask =  func_df['labels']
subs = func_df['subs']


condition_mask = func_df["labels"].isin(['app', 'unapp'])
#condition_mask = func_df["labels"].isin(['app', 'H2O'])
print(condition_mask.shape)
#y = y_mask[condition_mask]
y = y_mask[condition_mask]
print(y.shape)
n_conditions = np.size(np.unique(y))
print(n_conditions)
#n_conditions = np.size(np.unique(y))
print(y.unique())

session = func_df[condition_mask].to_records(index=False)
print(session.dtype.name)
#prepare the fxnl data.
nifti_masker = NiftiMasker(mask_img=imag_mask, smoothing_fwhm=4,standardize=True, memory_level=0)
fmri_trans = nifti_masker.fit_transform(fmri_subjs)
print(fmri_trans)
X = fmri_trans[condition_mask]
subs = subs[condition_mask]

svc = SVC(kernel='linear', verbose=False)
print(svc)

from sklearn.feature_selection import SelectPercentile, f_classif
feature_selection = SelectPercentile(f_classif, percentile=10)

anova_svc = Pipeline([('anova',feature_selection), ('svc',svc)])
#fit the decoder and predict
anova_svc.fit(X, y)
y_pred = anova_svc.predict(X)

np.warnings.filterwarnings('ignore')

cv = LeaveOneLabelOut(session)
cv_scores = cross_val_score(anova_svc, X, y, cv=cv)
classification_accuracy = cv_scores.mean()

print("Classification accuracy: %.4f / Chance level: %f" %
      (classification_accuracy, 1. / len(y.unique())))
