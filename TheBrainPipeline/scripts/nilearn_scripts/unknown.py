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
#make a list of the files to concat
all_func = glob.glob(os.path.join(basepath,'level1_grace_edit','cs*++.feat','filtered_func_data.nii.gz'))
half_func = all_func[:67]

fmri_subjs=os.path.join(outpath, 'concatenated_imagine_all.nii')
average_ana=os.path.join(outpath,'CS_avg_mprage_image.nii.gz')
imag_mask=os.path.join(outpath,'power_roimask_4bi.nii.gz')
#plot mask (Power ROIs) over anatomical that is defined above
#plotting.plot_roi(imag_mask,bg_img=average_ana,cmap='Paired')
#load labels for the functional data
#stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_67_sub.csv')
stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_all_sub.csv')

orig_data = pd.read_csv(stim, sep=",")
conditions = orig_data["label"] #'labels' for half_func

condition_mask = orig_data['label'].isin(['unapp', 'app', 'rest', 'H2O'])
conditions = conditions[condition_mask]

print(conditions.unique())
n_conditions = np.size(np.unique(conditions))
print(n_conditions)

session = orig_data[condition_mask].to_records(index=False)
print(session.dtype.names)


nifti_masker = NiftiMasker(mask_img=imag_mask,smoothing_fwhm=4,standardize=True, memory_level=1)
X = nifti_masker.fit_transform(fmri_subjs)
feature_selection = SelectKBest(f_classif, k=1500)
anova_svc = Pipeline([('anova', feature_selection), ('svc', svc)])
np.warnings.filterwarnings('ignore')
