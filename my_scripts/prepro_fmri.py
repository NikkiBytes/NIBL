#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 20:38:28 2018

@author: nikkibytes
"""
from multiprocessing import Pool
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import glob
import argparse
import os
import subprocess
import datetime



#__________________________________________________________________________________________________________________________
# Set (GLOBAL) directories **currently hardcoded

def check_output_directories(sub):
    # check for motion_assesment directory

    if not os.path.exists(os.path.join(derivatives_dir, sub)):
        os.makedirs(os.path.join(derivatives_dir, sub))
    if not os.path.exists(os.path.join(anat_output_path)):
        os.makedirs(os.path.join(anat_output_path))
    if not os.path.exists(os.path.join(func_output_path)):
        os.makedirs(os.path.join(func_output_path))
    if not os.path.exists(os.path.join(func_output_path,'motion_assessment')):
        os.makedirs(os.path.join(func_output_path,  'motion_assessment'))
    if not os.path.exists(os.path.join(func_output_path,'Analysis')):
        os.makedirs(os.path.join(func_output_path,  'Analysis'))

def set_paths(sub):
    global func_output_path
    global anat_output_path
    global input_bids_func_path
    global motion_assessment_path
    input_bids_func_path=os.path.join(input_dir,sub,'func')
    anat_output_path=os.path.join(derivatives_dir, sub, 'anat')
    func_output_path=os.path.join(derivatives_dir, sub, 'func')
    motion_assessment_path=os.path.join(derivatives_dir, sub, 'func','motion_assessment')


def get_subjects():
    global sub_dir
    global output_dir
    global input_dir
    global derivatives_dir
    global sub_dict
    sub_dict = {}

    # Get data from input
    #input_dir = input("Enter directory path of your subjects: ")
    #output_dir = input("Enter directory path for your output: ")
    input_dir = '/projects/niblab/bids_projects/Experiments/test'
    output_dir = '/projects/niblab/bids_projects/Experiments/test'
    derivatives_dir = os.path.join(output_dir, 'derivatives')
    sub_dir=glob.glob(os.path.join(input_dir, 'sub*'))
    os.chdir(input_dir)
    files = os.listdir('.')
    for file in files:
        if 'sub' in file:
            sub_dict[file] = None

    for sub in sub_dict:
        set_paths(sub)
        check_output_directories(sub)

def write_files():
    global datestamp
    global outhtml
    global out_bad_bold_list

    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    outhtml = os.path.join(derivatives_dir,'bold_motion_QA_%s.html'%(datestamp))
    out_bad_bold_list = os.path.join(derivatives_dir,'TEST_%s.txt'%(datestamp))



#__________________________________________________________________________________________________________________________
# Get dictionary of subjects from given directory

def set_parser():
    global parser
    global arglist
    global args
    parser=argparse.ArgumentParser(description='preprocessing')

    parser.add_argument('-task',dest='TASK',
                        default=False, help='which task are we running on?')
    parser.add_argument('-moco',dest='MOCO',
                        action="store_true", help='this is using fsl_motion_outliers to preform motion correction and generate a confounds.txt as well as DVARS')
    parser.add_argument('-bet',dest='STRIP',action='store_true',
                        default=False, help='bet via fsl using defaults for functional images')


    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
    print(arglist)

def split_list():
        half = len(sub_dir)/2
        return sub_dir[:int(half)], sub_dir[int(half):]
#__________________________________________________________________________________________________________________________




# def preproc()__________________________________________________________________________________________________________________________
# method to run preprocessing steps (functional bet, motion assessment)
# We pass into it -  DATA (a list of our subjects)

def preproc(DATA):

# BET__________________________________________________________________________________________________________
# ----> FOCUS: functional

    if args.STRIP==True:
        print("starting bet")
#        print("PRINTING DATA: \n", DATA, "\n")

        for sub in sub_dict:
            print("SUB: ", sub)
            set_paths(sub)
            os.chdir(input_bids_func_path)
            for nifti in glob.glob(os.path.join('sub-*_task-%s_bold.nii.gz')%(arglist['TASK'])):
              # make our variables
                output=nifti.strip('.nii.gz')
                bet_name=output+'_brain'
                # check if data exists already
                bet_output = os.path.join(func_output_path, bet_name)
                if os.path.exists(bet_output + '.nii.gz'):
                    print(bet_output + ' exists, skipping \n')
                else:
                    print("Running bet on ", nifti)
#                    print("BET COMMAND: ", bet_cmd, "\n")
                    bet_cmd=("bet %s %s -F -m"%(nifti, bet_output))
                #    os.system(bet_cmd)

        # lets check our variables
                print("VARIABLES:")
                print("SUB: ", sub)
                print("NIFTI: ", nifti)
                print("OUTPUT: ", output)
                print("BET OUTPUT: ", bet_output)
                print("__________________________________________________________________________________")


    if args.MOCO==False:
        print("skippin motion correction")
    else:
        print("---------> Starting motion correction")
        for sub in sub_dict:
            set_paths(sub)
        # decide which input path is being used [fmriprep or bids],
        # --note all directories may be different and may effect this pathing
        # --the path here connects the pathing to get the func folder:
        #       BIDS: { sub_dir + the sub# (sub-XX) + func }
        #       fMRIprep: { sub_dir + the sub# (sub-XX) + fmriprep + sub# (sub-XX) + func }

            os.chdir(func_output_path)
# iterate over nifti files
            for nifti in glob.glob(os.path.join('sub-*_task-%s_bold_brain.nii.gz')%(arglist['TASK'])):
                print("NIFTI: ", nifti)
                filename=nifti.split('.')[0]
                print("FILENAME: ", filename)
            # set comparison param
                cmd="fslnvols " + nifti
                volume = subprocess.check_output(cmd, shell=True, encoding="utf-8")
                volume = volume.strip()
                comparator = int(volume) *.25
                print("VOLUME: ", volume)
                print("Comparison: ", comparator)
                print("CMD:", cmd)
                os.system("fsl_motion_outliers -i %s  -o %s/%s_confound.txt  --fd --thresh=0.9 -p %s/fd_plot -v > %s/%s_outlier_output.txt"%(filename, motion_assessment_path, filename, motion_assessment_path, motion_assessment_path, filename))
                os.system("cat %s/%s_outlier_output.txt >> %s"%(motion_assessment_path, filename,outhtml))

           # Get the full path to the plot created by fsl_motion_outliers
                plotz=os.path.join(motion_assessment_path, 'fd_plot.png')

           # Create an html file based on plot
                os.system("echo '<p>=============<p>FD plot %s <br><IMG BORDER=0 SRC=%s WIDTH=%s></BODY></HTML>' >> %s"%(filename, plotz,'100%', outhtml))


           # Create a blank file
           # --sometimes you have a great subject who didn't move
                if os.path.isfile("%s/%s_confound.txt"%(motion_assessment_path, filename))==False:
                    os.system("touch %s/%s_confound.txt"%(motion_assessment_path, filename))

           # how many columns are there = how many 'bad' points
                check = subprocess.check_output("grep -o 1 %s/%s_confound.txt | wc -l"%(motion_assessment_path, filename), shell=True)

                num_scrub = [int(s) for s in check.split() if s.isdigit()]
                print("NUM SCRUB: ", str(num_scrub[0]), "\n")

                if num_scrub[0] > comparator: #if the number in check is greater than num_scrub then we don't want it
                    with open(out_bad_bold_list, "a") as myfile: #making a file that lists all the bad ones
                        myfile.write("%s/%s\n"%(derivatives_dir, filename))
                        print("wrote bad file")
                        myfile.close()




def main():

    get_subjects()

    write_files()

    set_parser()

    B, C = split_list()
    pool = Pool(processes=2)
    pool.map(preproc, [B,C])


#________________________________________________________________________________________________

# Start Program
if __name__ == "__main__":
    main()
