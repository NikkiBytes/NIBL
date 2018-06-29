#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 20:38:28 2018

@author: nikkibytes, extending from original by Dr. Grace Shearrer
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





#________________________________________________________________________________________
# This method, check_output_directories(sub), checks the ~/derivatives directory
# and will make relevant directories if we need to {anat/, func/, motion_assesment/ Analysis/},
# as an argument it takes the subject ID.
#________________________________________________________________________________________

def check_output_directories(sub):
    # check for motion_assesment directory

    if not os.path.exists(os.path.join(derivatives_dir, sub)):
        os.makedirs(os.path.join(derivatives_dir, sub))

    if arglist["SES"] != False:
        if not os.path.exists(os.path.join(derivatives_dir, sub, arglist["SES"])):
            os.makedirs(os.path.join(derivatives_dir, sub, arglist["SES"]))

    if not os.path.exists(os.path.join(anat_output_path)):
        os.makedirs(os.path.join(anat_output_path))
    if not os.path.exists(os.path.join(func_output_path)):
        os.makedirs(os.path.join(func_output_path))
    if not os.path.exists(os.path.join(func_output_path,'motion_assessment')):
        os.makedirs(os.path.join(func_output_path,  'motion_assessment'))
    if not os.path.exists(os.path.join(func_output_path,'Analysis')):
        os.makedirs(os.path.join(func_output_path,  'Analysis'))




#________________________________________________________________________________________
# The set_paths(sub) method assigns variables for our directory paths.
# [input (BIDS), output(anat, func, motion_assesment)]
# It takes the subject ID as an argument, and **it is called from get_subjects()
#________________________________________________________________________________________

def set_paths(sub):
    global func_output_path
    global anat_output_path
    global func_input_path
    global motion_assessment_path

    if arglist["SES"] == False:
        out_dir = os.path.join(derivatives_dir, sub)
    else:
        out_dir = os.path.join(derivatives_dir, sub, arglist["SES"])

    func_input_path=os.path.join(input_dir,sub,'func')
    anat_output_path=os.path.join(out_dir, 'anat')
    func_output_path=os.path.join(out_dir,'func')
    motion_assessment_path=os.path.join(out_dir,'func','motion_assessment')
    print("FUNC OUTPUT: ", func_output_path)

#________________________________________________________________________________________
# The get_subjects() method gets an input directory, the BIDS path, we ask for the "top level"
# BIDS directory, where the subjects are listed, ~/STUDYNAME.
# For the output directory we ask for you to provide the location where you would like
# your derivatives directory to be, or the path to its location, however do not include
# the derivatives directory.
#________________________________________________________________________________________


def get_subjects():
    global sub_dir
    global output_dir
    global input_dir
    global derivatives_dir
    global subjects
    subjects = []

    # Get data from input
    #input_dir = input("Enter directory path of your subjects: ")
    #output_dir = input("Enter directory path for your output: ")
    input_dir = '/Users/nikkibytes/Documents/Test/BIDS'
    output_dir = '/Users/nikkibytes/Documents/Test'
    derivatives_dir = os.path.join(output_dir, 'derivatives')
    if not os.path.exists(os.path.join(derivatives_dir)):
        os.makedirs(os.path.join(derivatives_dir))
    sub_dir=glob.glob(os.path.join(input_dir, 'sub*'))
    os.chdir(input_dir)
    files = os.listdir('.')
    for file in files:
        if 'sub' in file:
            subjects.append(file)
    print(subjects)
    for sub in subjects:
        set_paths(sub)
        check_output_directories(sub)



#________________________________________________________________________________________
# The write_files() method sets the file paths for output files
#________________________________________________________________________________________

def output_files():
    global datestamp
    global outhtml
    global out_bad_bold_list

    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")

    if arglist["SES"] == False:
        outhtml = os.path.join(derivatives_dir,'bold_motion_QA_%s.html'%(datestamp))
        out_bad_bold_list = os.path.join(derivatives_dir,'TEST_%s.txt'%(datestamp))
    else:
        outhtml = os.path.join(derivatives_dir,'%s_bold_motion_QA_%s.html'%(arglist["SES"],datestamp))
        out_bad_bold_list = os.path.join(derivatives_dir,'%s_TEST_%s.txt'%(arglist["SES"], datestamp))




#________________________________________________________________________________________

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
    parser.add_argument('-ses',dest='SES',
                        default=False, help='have multiple sessions?')


    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
    print(arglist)

def split_list():
        half = len(subjects)/2
        return subjects[:int(half)], subjects[int(half):]


#________________________________________________________________________________________

def preproc(data):

    if args.STRIP==True:
        print("starting bet")
        for sub in data:
            try:
                print("SUB: ", sub)
                set_paths(sub)
                os.chdir(func_input_path)

                for nifti in glob.glob(os.path.join('*bold.nii.gz')):
              # make our variables
                    output=nifti.strip('.nii.gz')
                    bet_name=output+'_brain'
                # check if data exists already
                    bet_output = os.path.join(func_output_path, bet_name)
                    if os.path.exists(bet_output + '.nii.gz'):
                        print(bet_output + ' exists, skipping \n')
                    else:
                        print("Running bet on ", nifti)
                        bet_cmd=("bet %s %s -F -m"%(nifti, bet_output))
                        os.system(bet_cmd)

        # lets check our variables
                    print("VARIABLES:")
                    print("SUB: ", sub)
                    print("NIFTI: ", nifti)
                    print("OUTPUT: ", output)
                    print("BET OUTPUT: ", bet_output)
                    print("__________________________________")
            except FileNotFoundError:
                print("BAD FILE PASSING")
                outfile = os.path.join(derivatives_dir, 'empty_subjects.txt')
                print(outfile)
                with open(outfile, 'a') as f:
                    f.write("Empty: %s \n "%(sub))
                    f.close()


    if args.MOCO==False:
        print(" -------------------> skipping motion correction")
    else:
        print("---------> Starting motion correction")
        try:
            for sub in data:
                set_paths(sub)
                os.chdir(func_output_path)
# iterate over nifti files

                for nifti in glob.glob('*brain.nii.gz'):
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
        except FileNotFoundError:
            print("FILE IS EMPTY, PASSING")


#________________________________________________________________________________________

def main():

    set_parser()
    get_subjects()

    output_files()



    B, C = split_list()
    pool = Pool(processes=2)


    pool.map(preproc, [B,C])


#________________________________________________________________________________________

# Start Program
if __name__ == "__main__":
    main()
