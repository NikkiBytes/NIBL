
import glob
import os
import fnmatch
import subprocess
#import pdb
import argparse
import shutil

#anat_input_path=input("Enter your anat input path: ")
basedir="/Users/nikkibytes/Documents/testing"

#deriv_path=input("Enter your derivatives path: ")
deriv_path="/Users/nikkibytes/Documents/testing/derivatives"

subjects=[]
os.chdir(deriv_path)
listOfSubjects = os.listdir('.')
for file in listOfSubjects:
    if 'sub-' in file:
        subjects.append(file)


for sub in subjects:
    fmriprep_path=os.path.join(basedir, 'fmriprep', sub, 'intermediate_results/fmriprep_wf/', 'single_subject_%s_wf'%(sub.split('-')[1]),'anat_preproc_wf/skullstrip_ants_wf/t1_skull_strip/*nii.gz')
    anat_output_path=os.path.join(deriv_path,sub,'anat')
    print("FMRIPREP PATH: ", fmriprep_path)
    print("OUTPUT PATH: ", anat_output_path)
    print("_____________________________________________________________________________________________")
    for file in glob.glob(fmriprep_path):
        print("NIFTI FILE: ", file, "\n")
        shutil.move(file, anat_output_path)


# move relevant data
#derivatives_dir = '/projects/niblab/bids_projects/Experiments/Bevel/data/derivatives'
#if not os.path.exists(os.path.join(derivatives_dir, sub, 'onsets')):
#    os.makedirs(os.path.join(derivatives_dir, sub, onsets))
