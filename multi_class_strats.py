
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

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


basepath=os.path.join('/projects','niblab','data','eric_data','W1','imagine')
outpath = "/projects/niblab/nilearn_projects"


# ---STEP 2---
#load & prepare MRI data
#load, fxnl, anatomical, & mask for plotting
fmri_subjs=os.path.join(outpath, 'concatenated_imagine_67.nii')
#fmri_subjs=os.path.join(outpath, 'concatenated_imagine_all.nii')
average_ana=os.path.join(outpath,'CS_avg_mprage_image.nii.gz')
imag_mask=os.path.join(outpath,'power_roimask_4bi.nii.gz')
#plot mask (Power ROIs) over anatomical that is defined above
#plotting.plot_roi(imag_mask,bg_img=average_ana,cmap='Paired')
#load labels for the functional data
stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_67_sub.csv')
#stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_all_sub.csv')

orig_data = pd.read_csv(stim, sep=",")
y = orig_data["labels"] #'labels' for half_func
session = orig_data["subs"] #'subs' for half_func

non_rest = (y != "rest")
y = y[non_rest]
non_trash = (y != "trash")
y = y[non_trash]


unique_conditions, order = np.unique(y, return_index=True)

unique_conditions = unique_conditions[np.argsort(order)]

nifti_masker = NiftiMasker(mask_img=imag_mask, sessions=session,smoothing_fwhm=4,standardize=True, memory_level=1)
