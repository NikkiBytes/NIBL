#!/usr/bin/env python

"""
Created on Fri Jun 15 13:57:30 EDT 2018

@author: nikkibytes, extending from original by Dr. Grace Shearrer
"""


import glob
import os
from subprocess import check_output
#import pdb
import argparse
import re

############################################################################################################
# SET PARSER
#
############################################################################################################.


def set_parser():

    global arglist

    parser=argparse.ArgumentParser(description='make your fsf files')
    parser.add_argument('-noreg',dest='NOREG', action='store_true',
                        default=False, help='Did you already register your data (using ANTZ maybe)?')
    parser.add_argument('-task',dest='TASK',
                        default=False, help='which functional task are we using?')


    parser.add_argument('-evs',dest='EV',nargs='+',
                        default=False, help='which evs are we using?')
    parser.add_argument('-runs',dest='RUN',nargs='+',
                        default=False, help='which run are we using?')
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]

############################################################################################################
# GET DIRECTORY PATHS
#
############################################################################################################.

def set_paths():
    global basedir
    global outdir
    global deriv_dir
    #basedir = input("Enter directory path of your subjects: ")
    #outdir = input("Enter directory path for your output: ")
    basedir='/Users/nikkibytes/Documents/testing'
    deriv_dir=os.path.join(basedir, 'derivatives')
    outdir=os.path.join(deriv_dir,'task')



############################################################################################################
# SET DICTIONARY METHOD
# here we are passed our subject parameter and we initialize our dictionary key, the subject,
# and fill it with another dictionary set with starting values.
############################################################################################################

def set_dict(sub):


    main_dict[sub] = {
            #'FUNCRUN': None,
            'TR': None,
            'OUTPUT': None,
            'ANAT': None,
         }


############################################################################################################
# CHECK REGISTRATION METHOD
#
############################################################################################################.


def check_registartion(sub):
    if arglist['NOREG']==False:
        with open(os.path.join(deriv_dir,'reg_design.fsf'),'r') as infile:
            tempfsf=infile.read()
            for key in main_dict:
                tempfsf = tempfsf.replace(key, main_dict[key])
                with open(os.path.join(outdir,sub,'%s_%s.fsf'%(sub,arglist['TASK'])),'w') as outfile:
                    outfile.write(tempfsf)
                outfile.close()
            infile.close()
## **** START EDIT HERE
    else:
        print("skipping registration")
        with open(os.path.join(deriv_dir,'design.fsf'),'r') as infile:
            tempfsf=infile.read()
            for key in main_dict:
                for run in arglist["RUN"]:
                    num=int(run)
                    print(num,  main_dict[key]["CONFOUND%i"%num])
                    tempfsf = tempfsf.replace("OUTPUT", main_dict[key]["OUTPUT"])
                    tempfsf = tempfsf.replace("FUNCRUN", main_dict[key]["FUNCRUN%i"%num]) #4D AVW DATA
                    tempfsf = tempfsf.replace("NTPTS", main_dict[key]["NTIMEPOINT%i"%num])
                    tempfsf = tempfsf.replace("CONFOUND", main_dict[key]["CONFOUND%i"%num])
                    for key2 in main_dict[key]:
                        if re.match(r'EV[0-9]TITLE', key2):
                            ev_title = main_dict[key][key2]
                            n = re.findall('\d+', key2)
                            n = ''.join(str(x) for x in n)
                            #print("EV%s"%n)
                            tempfsf = tempfsf.replace("EV%s"%n, main_dict[key]["EV%s"%n])
                        tempfsf = tempfsf.replace("MOCO0", main_dict[key]["MOCO0"])
                        tempfsf = tempfsf.replace("MOCO1", main_dict[key]["MOCO1"])
                        tempfsf = tempfsf.replace("MOCO2", main_dict[key]["MOCO2"])
                        tempfsf = tempfsf.replace("MOCO3", main_dict[key]["MOCO3"])
                        tempfsf = tempfsf.replace("MOCO4", main_dict[key]["MOCO4"])
                        tempfsf = tempfsf.replace("MOCO5", main_dict[key]["MOCO5"])
                    outpath= outdir+"/"+sub
                    if not os.path.exists(outpath):
                        os.makedirs(outpath)
                    with open(os.path.join(outpath,'%s_task-%s_run-%s_no_reg.fsf'%(sub,arglist['TASK'], run)),'w') as outfile:
                        outfile.write(tempfsf)
                        outfile.close()
                    infile.close()



############################################################################################################
# FILL DICTIONARY METHOD
# here we are updating our dictionary with relevant values
############################################################################################################

def fill_dict(subj):
    #print("SUBJ: ", subj)
    for sub in main_dict:
        #print(sub)

    # -- THE SUBEJCT
    #repl_dict.update({'SUB':sub})
        deriv_dir = '/Users/nikkibytes/Documents/testing/derivatives'
    # -- THE RUNS
        for run in arglist['RUN']:
            scan=(os.path.join( sub,'func','%s_task-%s_run-%s_bold_brain.nii.gz')%(sub,arglist['TASK'], run))
            funcrun=os.path.join(deriv_dir, scan)
            x=int(run)
            main_dict[sub]['FUNCRUN%i'%x] = funcrun
           # print("FUNCRUN: ", funcrun)

    # -- THE TIMEPOINTS -- found by running 'fslnvols' on our scan file
            ntmpts=check_output(['fslnvols', funcrun])
            ntmpts = ntmpts.decode('utf-8')
            ntmpts = ntmpts.strip('\n')
            main_dict[sub]['NTIMEPOINT%i'%x] = ntmpts
           # print("TIMEPOINT: ", ntmpts)

    # -- CONFOUNDS
            confounds=os.path.join(deriv_dir,sub,'func','motion_assessment','%s_task-%s_run-%s_bold_brain_confound.txt'%(sub,arglist['TASK'],x))
            main_dict[sub]['CONFOUND%i'%x] = confounds
          #  print("CONFOUNDS: ", confounds)

    # -- MOTION CORRECTION
            for i in range(6):
                motcor=os.path.join(sub,'func','motion_assessment', 'motion_parameters','%s_task-%s_run-%s_moco%s.txt' %(sub,arglist['TASK'],run,i))
                main_dict[sub]['MOCO%i'%i] = motcor
         #       print("MOTCOR: ", motcor)


    # -- TRS FROM NIFTI -- this value will always be 2, therefore we only run the check once
        trs=check_output(['fslval','%s'%(funcrun),'pixdim4',scan])
        trs=trs.decode('utf-8')
        trs=trs.strip('\n')
        #print("TRs: ", trs)
        main_dict[sub]['TR'] = trs


    # -- OUTPUT -- directory where output will go
        output=os.path.join(deriv_dir, sub, 'func', 'Analysis', 'task', arglist['TASK'])
        main_dict[sub]['OUTPUT'] = output
        #print("OUTPUT: ", output)


    # -- ANAT -- get the anat file for the subject, the syntax currently follows fmriprep standard
        anat=os.path.join(deriv_dir ,sub,'anat','highres001_BrainExtractionBrain.nii.gz')
        main_dict[sub]['ANAT'] = anat
        #print("ANAT: ", anat)


    # -- EVS -- here we loop through the given EVs and add the corresponding file to the dictionary

        ctr=0
        for item in arglist['EV']:
            #print(item)
            ctr=ctr+1
            main_dict[sub]['EV%iTITLE'%ctr] = item
            ev=os.path.join(sub,'func','onsets','%s_%s_%s.txt'%(sub,arglist['TASK'],item))
            #print("EV: ", ev)
            main_dict[sub]['EV%i'%ctr] = ev

############################################################################################################
# CREATE FSF FILE
#
############################################################################################################.

def create_fsf():
    os.chdir(deriv_dir)
    global main_dict
    main_dict= {}

    for sub in glob.glob('sub-*'):
        set_dict(sub)
        fill_dict(sub)
        check_registartion(sub)

############################################################################################################
# MAIN METHOD
#
############################################################################################################.


def main():
    set_parser()
    if not arglist["RUN"]:
        print("RUN list is empty")
    else:
        set_paths()
        create_fsf()
main()
