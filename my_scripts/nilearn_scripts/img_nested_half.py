
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

#n_conditions = np.size(np.unique(y))
print(y.unique())
#session = func_df[condition_mask].to_records(index=False)
#print(session.dtype.name)


# In[22]:


#prepare the fxnl data. 
nifti_masker = NiftiMasker(mask_img=imag_mask,
                           smoothing_fwhm=4,standardize=True,
                           memory="nilearn_cache",memory_level=1)

fmri_trans = nifti_masker.fit_transform(fmri_subjs)
#print(fmri_trans)
#X = fmri_trans[condition_mask]
#subs = subs[condition_mask]

