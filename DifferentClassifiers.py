"""
@author: nicholletteacosta

"""
import matplotlib.pyplot as plt
import os
import numpy as np
import nilearn
import glob
import pandas as pd
from nilearn import plotting
from nilearn.input_data import NiftiMasker

"""
# ---STEP 1---
# GET DATA
#Cncatenate the imagine data into a NIFTI-2 file.
#Note: the data does not fit into a NIFTI-1 file, due to large number of subs.
"""

#set basepath
basepath=os.path.join('/projects','niblab','data','eric_data','W1','imagine')
outpath = "/projects/niblab/nilearn_projects"
#make a list of the files to concat
all_func = glob.glob(os.path.join(basepath,'level1_grace_edit','cs*++.feat','filtered_func_data.nii.gz'))
half_func = all_func[:67]



"""
# ---STEP 2---
#load & prepare MRI data
#load, fxnl, anatomical, & mask for plotting

"""
fmri_subjs=os.path.join(outpath, 'concatenated_imagine_67.nii')
average_ana=os.path.join(outpath,'CS_avg_mprage_image.nii.gz')
imag_mask=os.path.join(outpath,'power_roimask_4bi.nii.gz')
#plot mask (Power ROIs) over anatomical that is defined above
#plotting.plot_roi(imag_mask,bg_img=average_ana,cmap='Paired')
#load labels for the functional data
stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_67_sub.csv')

#Its shape corresponds to the number of time-points times the number of voxels in the mask
# loading target information as string and give a numerical identifier to each
labels_df = pd.read_csv(stim, sep=",")
labels_df = labels_df[labels_df.labels != "trash"] #remove 'trash' data

#Retrieve the behavioral targets that we are going to predict in the decoding
#Restrict analysis to 'unapp', 'app', 'H2O'
stimuli =  labels_df['labels'] #Stimuli dataframe holds the string labels

# identify and remove resting state data
task_mask = (stimuli != 'rest')

# find the names of remaining labels 
categories = stimuli[task_mask].unique()

#extract tags indicating to which acquisition run a tag belongs
session_labels = labels_df["subs"][task_mask]



nifti_masker = NiftiMasker(mask_img=imag_mask, smoothing_fwhm=4,standardize=True)
masked_timecourses = nifti_masker.fit_transform(fmri_subjs)[task_mask]
