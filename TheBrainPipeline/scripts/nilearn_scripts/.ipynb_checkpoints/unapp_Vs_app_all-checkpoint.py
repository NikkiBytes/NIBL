"""
@author: jennygilbert extended upon by nicholletteacosta

"""
#%matplotlib inline
import os
import numpy as np
import nilearn
import glob
import matplotlib.pyplot as plt
import nibabel as nib
import pandas as pd
from nilearn.image import concat_imgs, index_img, smooth_img
from nilearn.image import resample_to_img
from nilearn import plotting
from nilearn.input_data import NiftiMasker
from sklearn.svm import SVC
from sklearn.model_selection import LeaveOneOut, cross_val_score, permutation_test_score
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from nilearn import image
from nilearn.plotting import plot_stat_map, show
from sklearn.dummy import DummyClassifier

# In[4]:

"""
# ---STEP 1---
# Concatenate the imagine data into a NIFTI-2 file. (--if not done already)
# Note: the data does not fit into a NIFTI-1 file, due to large number of subs.
"""
#set basepath
basepath=os.path.join('/projects','niblab','data','eric_data','W1','imagine')
#basepath ='/projects/niblab/nilearn_projects'
outpath = "/projects/niblab/nilearn_projects"
#make a list of the files to concat
all_func = glob.glob(os.path.join(basepath,'level1_grace_edit','cs*++.feat','filtered_func_data.nii.gz'))
len(all_func)
half_func = all_func[:67]
half2_func= all_func[67:]


"""
#load in all the files from the glob above, then convert them from nifti1 to nifti2
ni2_funcs = (nib.Nifti2Image.from_image(nib.load(func)) for func in all_func)
#concat, this is with nibabel, but should work with nilearn too
ni2_concat = nib.concat_images(ni2_funcs, check_affines=False, axis=3)
#set the output file name
outfile=os.path.join(outpath,'concatenated_imagine_all.nii')
#write the file
ni2_concat.to_filename(outfile)
"""
fmri_subjs=os.path.join(outpath, 'concatenated_imagine_all.nii')
average_ana=os.path.join(outpath,'CS_avg_mprage_image.nii.gz')
imag_mask=os.path.join(outpath,'power_roimask_4bi.nii.gz')
stim = os.path.join('/projects','niblab','scripts','nilean_stuff','label_all_sub.csv')
func_df = pd.read_csv(stim, sep=",")
y_mask =  func_df['label']
subs = func_df['sub']



"""
# ---STEP 3---
# Feature Selection
# To keep only data corresponding to app food or unapp food, we create a mask of the samples
# belonging to the condition.
"""
#condition_mask = np.logical_or(y_mask == b'app',y_mask == b'unapp')
condition_mask = func_df["label"].isin(['app', 'unapp'])
print(condition_mask.shape)
#y = y_mask[condition_mask]
y = y_mask[condition_mask]
print(y.shape)
n_conditions = np.size(np.unique(y))
print(n_conditions)
#n_conditions = np.size(np.unique(y))
print(y.unique())
nifti_masker = NiftiMasker(mask_img=imag_mask, smoothing_fwhm=4,standardize=True)
fmri_trans = nifti_masker.fit_transform(fmri_subjs)
print(fmri_trans)
X = fmri_trans[condition_mask]
subs = subs[condition_mask] # equivalent to 'session'

"""
# ---STEP 4---
# Build the Decoder
# Define the dimension reduction to be used.
# Here we use a classical univariate feature selection based on F-test, namely Anova.
# We set the number of features to be selected to 500
# SelectKBest removes all but the k highest scoring features
# We have our classifier (SVC), our feature selection (SelectKBest), and now,
# we can plug them together in a *pipeline* that performs the two operations successively:
"""
svc = SVC()
print(svc)

feature_selection = SelectPercentile(f_classif, percentile=5)
feature_selection = SelectKBest(f_classif, k=3000)
anova_svc = Pipeline([('anova',feature_selection), ('svc',svc)])

"""
# ---STEP 5---
# Compute Prediction Scores using Cross-Validation
# Fit the decoder and predict.
"""
anova_svc.fit(X, y)
y_pred = anova_svc.predict(X)
cv = LeaveOneLabelOut(subs[subs<1])
k_range = [10, 15, 30, 50 , 150, 300, 500, 1000, 1500, 3000, 5000]
#cv_scores = cross_val_score(anova_svc, X[subs ==1], y[subs ==1])
scores_validation = []
cv_scores = []
#classification_accuracy = cv_scores.mean()
#print("Classification accuracy: %.4f / Chance level: %f" %
#      (classification_accuracy, 1. / n_conditions))
for k in k_range:
    feature_selection.k = k
    cv_scores.append(np.mean(cross_val_score(anova_svc, X[subs==1], y[subs==1])))
    print("CV score: %.4f" % cv_scores[-1])
    anova_svc.fit(X[subs ==1], y[subs == 1])
    y_pred = anova_svc.predict(X[subs == 0])
    scores_validation.append(np.mean(y_pred == y[subs == 0]))
    print("score validation: %.4f" % scores_validation[-1])
"""
# ---STEP 6---
# Nested Cross-Validation
# We are going to tune the parameter 'k' of the step called 'anova' in the pipeline.
# Thus we need to address it as 'anova__k'. we are working with a composite estimator:
# -- a pipeline of feature selection followed by SVC. Thus to give the name of the parameter
# that we want to tune we need to give the name of the step in
# the pipeline, followed by the name of the parameter, with ‘__’ as a separator.
# Note that GridSearchCV takes an n_jobs argument that can make it go much faster
"""
grid = GridSearchCV(anova_svc, param_grid={'anova__k': k_range},n_jobs=2, verbose=1)
nested_cv_scores = cross_val_score(grid, X, y)
class_accuracy = np.mean(nested_cv_scores)
print("Nested CV score: %.4f" %(class_accuracy))

"""
# Plot the Prediction Scores
"""
plt.figure(figsize=(6, 4))
plt.plot(cv_scores, label='Cross validation scores')
plt.plot(scores_validation, label='Left-out validation data scores')
plt.xticks(np.arange(len(k_range)), k_range)
plt.axis('tight')
plt.xlabel('k')

plt.axhline(np.mean(nested_cv_scores),
            label='Nested cross-validation',
            color='r')

plt.legend(loc='best', frameon=False)
plt.show()
