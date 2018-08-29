
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

# ---STEP 1---
#Cncatenate the imagine data into a NIFTI-2 file.
#Note: the data does not fit into a NIFTI-1 file, due to large number of subs.

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


#condition_mask = y.isin(['app', 'unapp'])
condition_mask = y.isin(['unapp', 'H2O'])
y = y[condition_mask]



n_conditions = np.size(np.unique(y))
print(n_conditions)
nifti_masker = NiftiMasker(mask_img=imag_mask, sessions=session,smoothing_fwhm=4,standardize=True, memory_level=1)
X = nifti_masker.fit_transform(fmri_subjs)
print(X)
X = X[condition_mask]
session = session[condition_mask]


np.warnings.filterwarnings('ignore')


from sklearn.svm import SVC
#svc = SVC(verbose=False)
svc = SVC(kernel='linear', verbose=False)

feature_selection = SelectKBest(f_classif, k=500)
anova_svc = Pipeline([('anova', feature_selection), ('svc', svc)])
np.warnings.filterwarnings('ignore')
k_range = [10, 15, 30, 50, 150, 300, 500, 1000, 1500, 3000, 5000]
cv_scores = []
scores_validation = []
for k in k_range:
    feature_selection.k = k
    cv_scores.append(np.mean(cross_val_score(anova_svc, X[session < 1], y[session < 1])))
    print("CV score: %.4f" % cv_scores[-1])
    anova_svc.fit(X[session < 1], y[session < 1])
    y_pred = anova_svc.predict(X[session == 1])
    scores_validation.append(np.mean(y_pred == y[session == 1]))
    print("score validation: %.4f" % scores_validation[-1])


grid = GridSearchCV(anova_svc, param_grid={'anova__k': k_range}, verbose=1, n_jobs=2)
nested_cv_scores = cross_val_score(grid, X, y)
classification_accuracy = np.mean(nested_cv_scores)
print("Classification accuracy: %.4f / Chance level: %f" %(classification_accuracy, 1. / n_conditions))


plt.figure(figsize=(6, 4))
plt.plot(cv_scores, color="#33ccff",label='Cross validation scores')
plt.plot(scores_validation, color="#bf00ff", label='Left-out validation data scores')
plt.xticks(np.arange(len(k_range)), k_range)
plt.axis('tight')
plt.xlabel('k')
plt.ylabel('%')
plt.title("CV For H2O vs. Unapp w/ linear kernel (67 subjects) ")
plt.axhline(np.mean(nested_cv_scores),
            label='Nested cross-validation',
            color='#33cc33')

plt.legend(loc='upper left',bbox_to_anchor=(1.04,1))
plt.show()
plt.savefig("/projects/niblab/nilearn_projects/h2O_vs_unapp_CV_67", bbox_inches = "tight" )
