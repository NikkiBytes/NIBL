
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
np.warnings.filterwarnings('ignore')


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
X = nifti_masker.fit_transform(fmri_subjs)


X = X[non_rest]
session = session[non_rest]

X = X[non_trash]
session = session[non_trash]

from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
svc_ovo = OneVsOneClassifier(Pipeline([
    ('anova', SelectKBest(f_classif, k=500)),
    ('svc', SVC(kernel='linear'))
]))

svc_ova = OneVsRestClassifier(Pipeline([
    ('anova', SelectKBest(f_classif, k=500)),
    ('svc', SVC(kernel='linear'))
]))


cv_scores_ovo = cross_val_score(svc_ovo, X, y, cv=5, verbose=1)

cv_scores_ova = cross_val_score(svc_ova, X, y, cv=5, verbose=1)

print('OvO:', cv_scores_ovo.mean())
print('OvA:', cv_scores_ova.mean())


plt.figure(figsize=(6,4))
plt.boxplot([cv_scores_ova, cv_scores_ovo])
plt.xticks([1, 2], ['One vs All', 'One vs One'])
plt.title('Prediction: accuracy score')
plt.show()
plt.savefig("/projects/niblab/nilearn_projects/multi-class_strats_box_whisker_plot", bbox_inches = "tight" )



from sklearn.metrics import confusion_matrix
from nilearn.plotting import plot_matrix

svc_ovo.fit(X[session < 1], y[session < 1])
y_pred_ovo = svc_ovo.predict(X[session >= 1])

plot_matrix(confusion_matrix(y_pred_ovo, y[session >= 1]),labels=unique_conditions, cmap='plasma')
plt.title('Confusion matrix: One vs One')
plt.show()
plt.savefig("/projects/niblab/nilearn_projects/multi-class_strats_confusion_matrix_OvO", bbox_inches = "tight" )
svc_ova.fit(X[session < 1], y[session < 1])
y_pred_ova = svc_ova.predilsct(X[session >= 1])

plot_matrix(confusion_matrix(y_pred_ova, y[session >= 1]),
            labels=unique_conditions, cmap='plasma')
plt.title('Confusion matrix: One vs All')
plt.show()
plt.savefig("/projects/niblab/nilearn_projects/multi-class_strats_confusion_matrix_OvA", bbox_inches = "tight" )
