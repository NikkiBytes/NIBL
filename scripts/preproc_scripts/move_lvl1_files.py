"""
Created on Fri Jun 15 13:57:30 EDT 2018

@author: nikkibytes

This script has initially been intended to automate the creation of directories,
and sorting relevant data together, for Feature Analysis

"""




import glob
import os
import fnmatch
import subprocess
#import pdb
import argparse
import shutil



# THE SET PATHS INITIALIZES AND SETS OUR INPUT/OUTPUT PATHS
# !-- CURRENTLY THE PROGRAM ASSUMES WE HAVE THE ~/derivatives DIRECTORY

def set_paths():
    print ("STARTING PROGRAM, GETTING VARIABLES....")
    global basedir
    global deriv_path
    global subjects
    #basedir=input("Enter your base directory input path: ")
    basedir="/projects/niblab/bids_projects/Experiments/EricData/data"
    #deriv_path=input("Enter your derivatives path: ")
    deriv_path=os.path.join(basedir, "derivatives")
    subjects = glob.glob("/projects/niblab/bids_projects/Experiments/EricData/data/fmriprep/sub-*")
    print(subjects)
    """subjects=[]
    os.chdir(deriv_path)
    listOfSubjects = os.listdir('.')
    for file in listOfSubjects:
        if 'sub-' in file:
            subjects.append(file)
    """

# THE MOVE_ANATS METHOD MOVES OUR NIFTI FILES FROM FMRIPREP INTO OUR ~/derivatives directory
# !-- MAY NEED TO COPY FILES (TO KEEP elFMRIPREP?)
def move_anats():
    errors = []
    print ("STARTING THE MOVE FILES PROCESS.........")
    for sub_file in subjects:
        sub = sub_file.split("/")[-1]
        print("SUBJECT >>>> %s \nSUBJECT FILE >>>> %s" %(sub, sub_file))
        #/EricData/data/fmriprep/sub-152/ses-2/fmriprep_wf
        #/single_subject_152_wf/anat_preproc_wf/skullstrip_ants_wf/t1_skull_strip
        fmriprep_path=os.path.join(sub_file, 'ses-2', 'fmriprep_wf/', 'single_subject_*','anat_preproc_wf/skullstrip_ants_wf/t1_skull_strip/*nii.gz')
        anat_output_path=os.path.join(deriv_path,sub, 'ses-2', 'anat')
        #print("OUTPUT PATH: ", anat_output_path)
        for file in glob.glob(fmriprep_path):
            try:
                #print("Moving file, %s , into directory located at, %s \n"%(file, anat_output_path))
                #shutil.move(file, anat_output_path)
                print("Copying file  %s ---------------------------------------> %s \n"%(file, anat_output_path))
                shutil.copy(file, anat_output_path)
            except shutil.Error as error:
                errors.extend(error.args[0])
                print(">>>>>>>>>>>>ERRROR")


set_paths()
move_anats()



# move relevant data
#derivatives_dir = '/projects/niblab/bids_projects/Experiments/Bevel/data/derivatives'
#if not os.path.exists(os.path.join(derivatives_dir, sub, 'onsets')):
#    os.makedirs(os.path.join(derivatives_dir, sub, onsets))
