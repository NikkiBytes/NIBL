#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 20:38:28 2018

@author: nikkibytes
"""

#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import glob
import argparse
import os
import subprocess
import datetime
from multiprocessing import Pool


#__________________________________________________________________________________________________________________________
# Set (GLOBAL) directories **currently hardcoded



def get_subjects()):
    global sub_dir
    global input_dir
    global sub_dict
    sub_dict = {}

    # Get data from input
    #input_dir = input("Enter directory path of your subjects: ")
    input_dir = '/Users/nikkibytes/Documents/testing/BIDS'
    sub_dir=glob.glob(os.path.join(input_dir, 'sub*'))
    os.chdir(input_dir)
    files = os.listdir('.')
    for file in files:
        if 'sub' in file:
            sub_dict[file] = None

def write_files():
    global datestamp
    global outhtml
    global out_bad_bold_list

    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    outhtml = os.path.join(input_dir,'bold_motion_QA_%s.html'%(datestamp))
    out_bad_bold_list = os.path.join(input_dir,'TEST_%s.txt'%(datestamp))


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
        return a_list[:int(half)], a_list[int(half):]
#__________________________________________________________________________________________________________________________
# Get data

#__________________________________________________________________________________________________________________________
# Get Data
# -- dictionary of subjects from given directory
# currently this assumes the data is listed in the sub-XX folder of a given directory path
# any input in the directory given containing 'sub*' will be included as a data directory
# ----------> MODIFY FOR FLEXIBILITY/REPRODUCIBILITY






# def preproc()__________________________________________________________________________________________________________________________
# method to run preprocessing steps (functional bet, motion assessment)
# We pass into it -  DATA (a list of our subjects)

def preproc(DATA):

# BET__________________________________________________________________________________________________________
# ----> FOCUS: functional

    if args.STRIP==True:
        print("starting bet")
        print("PRINTING DATA: \n", DATA, "\n")

        #for sub in DATA:
        for nifti in glob.glob(os.path.join('func', 'sub-*_task-%s_bold.nii.gz')%(arglist['TASK'])):
            # make our variables
            output=nifti.strip('.nii.gz')
            BET_OUTPUT=output+'_brain'
            # check if data exists already
            if os.path.exists(BET_OUTPUT):
                print(BET_OUTPUT + ' exists, skipping \n')
            else:
                print("Running bet on ", nifti)
                print("BET COMMAND: ", bet_cmd, "\n")
                bet_cmd=("bet %s %s -F -m"%(nifti, BET_OUTPUT))
                os.system(bet_cmd)

        # lets check our variables
            print("VARIABLES:")
            print("SUB: ", sub)
            print("NIFTI: ", nifti)
            print("OUTPUT: ", output)
            print("BET OUTPUT: ", BET_OUTPUT)
            print("__________________________________________________________________________________")


    if args.MOCO==False:
        print("skippin motion correction")
    else:
        print("---------> Starting motion correction")
        for sub in sub_dict:

        # decide which input path is being used [fmriprep or bids],
        # --note all directories may be different and may effect this pathing
        # --the path here connects the pathing to get the func folder:
        #       BIDS: { sub_dir + the sub# (sub-XX) + func }
        #       fMRIprep: { sub_dir + the sub# (sub-XX) + fmriprep + sub# (sub-XX) + func }

            #fmriprep_func_path=os.path.join(sub_dir,sub, 'fmriprep', id ,'func')
            bids_func_path=os.path.join(input_dir,sub,'func')
# change to func directory
            os.chdir(bids_func_path)
# check for motion_assesment directory
            if not os.path.exists(os.path.join(dir,'motion_assessment')): #looking for a motion assessment dir to put out put in, I like to put it in my functional directory where my skull stripped brain is
                os.makedirs(os.path.join(dir,'motion_assessment')) #making dir if it doesn't exist
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
                os.system("ls")
                os.system("fsl_motion_outliers -i %s  -o motion_assessment/%s_confound.txt  --fd --thresh=0.9 -p motion_assessment/fd_plot -v > motion_assessment/%s_outlier_output.txt"%(filename,filename, filename))
                os.system("cat motion_assessment/%s_outlier_output.txt >> %s"%(filename,outhtml))

           # Get the full path to the plot created by fsl_motion_outliers
                plotz=os.path.join(bids_func_path, 'motion_assessment','fd_plot.png')

           # Create an html file based on plot
                os.system("echo '<p>=============<p>FD plot %s <br><IMG BORDER=0 SRC=%s WIDTH=%s></BODY></HTML>' >> %s"%(filename, plotz,'100%', outhtml))


           # Create a blank file
           # --sometimes you have a great subject who didn't move
                if os.path.isfile("motion_assesment/%s_confound.txt"%(filename))==False:
                    os.system("touch motion_assessment/%s_confound.txt"%(filename))

           # how many columns are there = how many 'bad' points
                check = subprocess.check_output("grep -o 1 motion_assessment/%s_confound.txt | wc -l"%(filename), shell=True)

                num_scrub = [int(s) for s in check.split() if s.isdigit()]
                print("NUM SCRUB: ", str(num_scrub[0]), "\n")

                if num_scrub[0] > comparator: #if the number in check is greater than num_scrub then we don't want it
                    with open(out_bad_bold_list, "a") as myfile: #making a file that lists all the bad ones
                        myfile.write("%s\n"%(filename))
                        print("wrote bad file")
                        myfile.close()




def main():
    get_subjects()
    write_files()
    set_parser()

    print("SUBJECT DICTIONARY: ", sub_dict, "\n")
    #for key in sub_dict:
     #   print(key)
        #test dictionary

    B, C = split_list()
    pool = Pool(processes=2)
    pool.map(preproc, [B,C])
    #preproc(DATA)

#________________________________________________________________________________________________
# Start Program

# intiate with data grab and split



# begin parallel process, prompt main
#if __name__ == "__main__":
#    pool = Pool(processes=2)
#    pool.map(main, [B,C])

main()
