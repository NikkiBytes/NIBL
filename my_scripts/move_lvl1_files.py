
import glob
import os
import fnmatch
import subprocess
#import pdb
import argparse
import shutil


def set_paths():
    print ("STARTING PROGRAM, GETTING VARIABLES....")

    global basedir
    global deriv_path
    global subjects

    #basedir=input("Enter your base directory input path: ")
    basedir="/Users/nikkibytes/Documents/testing"

    #deriv_path=input("Enter your derivatives path: ")
    deriv_path="/Users/nikkibytes/Documents/testing/derivatives"

    subjects=[]
    os.chdir(deriv_path)
    listOfSubjects = os.listdir('.')
    for file in listOfSubjects:
        if 'sub-' in file:
            subjects.append(file)

def move_anats():
    errors = []
    print ("STARTING THE MOVE FILES PROCESS.........")

    for sub in subjects:
        fmriprep_path=os.path.join(basedir, 'fmriprep', sub, 'intermediate_results/fmriprep_wf/', 'single_subject_%s_wf'%(sub.split('-')[1]),'anat_preproc_wf/skullstrip_ants_wf/t1_skull_strip/*nii.gz')
        anat_output_path=os.path.join(deriv_path,sub,'anat')
        #print("FMRIPREP PATH: ", fmriprep_path)
        #print("OUTPUT PATH: ", anat_output_path)
        for file in glob.glob(fmriprep_path):
            print("Moving file, %s , into directory located at, %s \n"%(file, anat_output_path))
            try:
                shutil.move(file, anat_output_path)
            except shutil.Error as error:
                errors.extend(error.args[0])
                print("SHUTIL ERRROR, FILE ALREADY EXISTS")


set_paths()
move_anats()

# move relevant data
#derivatives_dir = '/projects/niblab/bids_projects/Experiments/Bevel/data/derivatives'
#if not os.path.exists(os.path.join(derivatives_dir, sub, 'onsets')):
#    os.makedirs(os.path.join(derivatives_dir, sub, onsets))
