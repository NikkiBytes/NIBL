#!/usr/bin/env python3
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



#__________________________________________________________________________________________________________________________
# Set (GLOBAL) directories **currently hardcoded


def set_directories():
    global func_keyword
    global basedir
    global datestamp
    global writedir
    global outhtml
    global out_bad_bold_list

    #global func_keyword = input("Please enter a keyword for the files in your func folder (Please use a wildcard(*)): \n i.e. *bold.nii.gz \n Enter: ")
    func_keyword = '*bold.nii.gz'


    basedir='/Users/gracer/Desktop/data'
    writedir='/Users/gracer/Desktop/data'

    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    outhtml = os.path.join(writedir,'bold_motion_QA_%s.html'%(datestamp))
    out_bad_bold_list = os.path.join(writedir,'lose_gt_45_vol_scrub_%s.txt'%(datestamp))


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

#__________________________________________________________________________________________________________________________
# Get data

#__________________________________________________________________________________________________________________________
# Get Data
# -- dictionary of subjects from given directory
# currently this assumes the data is listed in the sub-XX folder of a given directory path
# any input in the directory given containing 'sub*' will be included as a data directory
# ----------> MODIFY FOR FLEXIBILITY/REPRODUCIBILITY


def get_subjects(sub_dict):
    global sub_dir

    # Get data from input
    #sub_dir = input("Enter directory path of your subjects: ")
    sub_dir = '/Users/nikkibytes/Documents/testing/BIDS'
    os.chdir(sub_dir)
    files = os.listdir('.')
    for file in files:
        if 'sub' in file:
            sub_dict[file] = None




#__________________________________________________________________________________________________________________________
# method to run preprocessing steps (functional bet, motion assessment)

def preproc(DATA):
    #iterate over the subjects
#def better(args,arglist,basedir):

#_______________________________________________________BET___________________________________________________
# ----> FOCUS: functional

def preproc(DATA):
    if args.MOCO==False:
        print("please set a threshold for the FD, a good one is 0.9")
    else:
        print("starting motion correction")

    if args.STRIP==True:
        print("starting bet")
        print("PRINTING DATA: \n", DATA. "\n")
        #os.chdir(os.path.join(basedir))
        for sub in DATA:
            for nifti in glob.glob(os.path.join(sub, 'func', 'sub-*_task-%s_bold.nii.gz')%(arglist['TASK'])):
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
                #    os.system(bet_cmd)

        # lets check our variables
                print("VARIABLES:")
                print("SUB: ", sub)
                print("NIFTI: ", nifti)
                print("OUTPUT: ", output)
                print("BET OUTPUT: ", BET_OUTPUT)
                print("__________________________________________________________________________________")


#______________________________________________________MOTION CORRECTION_________________________________________

    if args.MOCO==False:
        print("skippin motion correction")
    else:
        print("starting motion correction")
        for sub in sub_dict:
            id = sub

        # decide which input path is being used [fmriprep or bids],
        # --note all directories may be different and may effect this pathing
            #fmriprep_func_path=os.path.join(sub_dir,id, 'fmriprep', id ,'func')
            bids_func_path=os.path.join(sub_dir,id,'func')

        # iterate over functional data
            for dir in glob.glob(bids_func_path):#path to the functional, skull stripped data
                print("DIRECTORY: ", dir)#not needed but i get crazy

        # move to the func directory
                os.chdir(dir)


        # check for motion_assesment directory
                if not os.path.exists(os.path.join(dir,'motion_assessment')): #looking for a motion assessment dir to put out put in, I like to put it in my functional directory where my skull stripped brain is
                    os.makedirs(os.path.join(dir,'motion_assessment')) #making dir if it doesn't exist

        # getting user input filename variable

                for func_input in glob.glob(os.path.join(func_keyword)):
                    task = func_input.split('.')[0]



         # set input/output path

                    fsl_input = os.path.join(dir, func_input)


         # set comparison param
                    cmd="fslnvols " + func_input
                    volume = subprocess.check_output(cmd, shell=True, encoding="utf-8")
                    volume = volume.strip()
                    comparator = int(volume) *.25

                    print("Identifier: ", id)
                    print("TASK: ", task)
                    print("FUNC FILE(Input): ", func_input)
                    print("VOLUME: ", volume)
                    print("Comparison: ", comparator)
                    print("CMD:", cmd)
                    print("FSL INPUT: ", fsl_input)
                    print("OUTPUT: ", output)
                    print("OUTHTML: ", outhtml)



           # Now we're running fsl_motion_outliers
           # this is generating the fd confounds txt, it is using the fd metric,
           # making a plot and putting it in the motion assessment directory we made above
                    os.system("fsl_motion_outliers -i %s  -o %s/%s_confound.txt  --fd --thresh=0.9 -p motion_assessment/fd_plot -v > %s/%s_outlier_output.txt"%(task, output,task,output, task))

                    os.system("cat motion_assessment/%s_outlier_output.txt >> %s"%(task,outhtml))

           # Get the full path to the plot created by fsl_motion_outliers
                    plotz=os.path.join(output,'fd_plot.png')

           # Create an html file based on plot
                    os.system("echo '<p>=============<p>FD plot %s <br><IMG BORDER=0 SRC=%s WIDTH=%s></BODY></HTML>' >> %s"%(task,plotz,'100%', outhtml))


           # Create a blank file
           # --sometimes you have a great subject who didn't move
                    if os.path.isfile("%s/%s_confound.txt"%(output,task))==False:
                        os.system("touch motion_assessment/%s_confound.txt"%(task))

           # how many columns are there = how many 'bad' points
                    check = subprocess.check_output("grep -o 1 %s/%s_confound.txt | wc -l"%(output, task), shell=True)

                    num_scrub = [int(s) for s in check.split() if s.isdigit()]
                    print("NUM SCRUB: ", str(num_scrub[0]), "\n")

                    if num_scrub[0] > comparator: #if the number in check is greater than num_scrub then we don't want it
                        with open(out_bad_bold_list, "a") as myfile: #making a file that lists all the bad ones
                            myfile.write("%s\n"%(task))
                            print("wrote bad file")
                            myfile.close()


def main():

    get_subjects()
    B, C = split_list(all_data)


    sub_dict ={}

    set_directories()

    set_parser()


    get_subjects(sub_dict) #,sub_dir)

    print("SUBJECT DICTIONARY: ", sub_dict)
    #for key in sub_dict:
     #   print(key)
        #test dictionary

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

#main()
