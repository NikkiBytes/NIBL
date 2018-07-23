"""
@author: jennygilbert extended upon by nicholletteacosta

"""

import os
import numpy as np
import nilearn
import glob
import matplotlib.pyplot as plt
import nibabel as nib
import pandas as pd

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
len(all_func)
#half_func = all_func[:67]


"""
load in all the files from the glob above, then convert them from nifti1 to nifti2
ni2_funcs = (nib.Nifti2Image.from_image(nib.load(func)) for func in all_func)
#concat, this is with nibabel, but should work with nilearn too
ni2_concat = nib.concat_images(ni2_funcs, check_affines=False, axis=3)
#set the output file name
outfile=os.path.join(outpath,'concatenated_imagine_all.nii')
#write the file
ni2_concat.to_filename(outfile)
"""
