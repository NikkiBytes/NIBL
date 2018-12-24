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
import os
import subprocess
import datetime

                
def get_subjects(sub_dir, sub_dict):
    os.chdir(sub_dir)
    files = os.listdir('.')
    for file in files:
        if 'sub' in file:
            sub_dict[file] = None

def preproc(sub_dict, sub_dir, func_keyword):
    for sub in sub_dict:
        id = sub
        #fmriprep_func_path=os.path.join(sub_dir,id, 'fmriprep', id ,'func')
        bids_func_path=os.path.join(sub_dir,id,'func')

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
                datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
                output = os.path.join(dir, 'motion_assessment')
                fsl_input = os.path.join(dir, func_input)
                outhtml = os.path.join(dir,'bold_motion_QA_test_%s.html'%(datestamp))
                out_bad_bold_list = os.path.join(output,'testing_%s.txt'%(datestamp))

           
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
    
    sub_dict ={}
    sub_dir = input("Enter directory path of your subjects: ")
    #sub_dir = '/Users/nikkibytes/Documents/testing/BIDS'
    func_keyword = input("Please enter a keyword for the files in your func folder (Please use a wildcard(*)): \n i.e. *bold.nii.gz \n Enter: ")
    #func_keyword = '*bold.nii.gz'
    #initialize dict subject
    get_subjects(sub_dir, sub_dict)
    
    print("SUBJECT DICTIONARY: ", sub_dict)
    #for key in sub_dict:
     #   print(key)
        #test dictionary
    
    
    preproc(sub_dict, sub_dir, func_keyword)
main()


    
