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
    parser.add_argument('-task',dest='TASK', nargs='+',
                        default=False, help='which functional task are we using?')
    parser.add_argument('-evs',dest='EV',nargs='+',
                        default=False, help='which evs are we using?')
    parser.add_argument('-runs',dest='RUN',nargs='+',
                        default=False, help='which run are we using?')
    parser.add_argument('-multisess',dest='MULTI_SESS', action='store_true',
                        default=False, help='Do you have multiple sessions? (True or False)')
    parser.add_argument('-sessions ',dest='SESS',
                        default=False, help='which ses are we using?')
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
    #basedir = input("Enter directory path of your data: ")
    #outdir = input("Enter directory path for your output: ")
    basedir='/projects/niblab/bids_projects/Experiments/EricData/data'
    deriv_dir=os.path.join(basedir, 'derivatives')
    outdir=os.path.join(deriv_dir)

############################################################################################################
# SET DICTIONARY METHOD
# here we are passed our subject parameter and we initialize our dictionary key, the subject,
# and fill it with another dictionary set with starting values.
############################################################################################################

def set_dict(sub):
    main_dict[sub] = { }
def fill_keys(task, sub):
    main_dict[sub][task] = {}


############################################################################################################
# CHECK REGISTRATION METHOD
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
        print("skipping registration......")
        for sub in main_dict: #iterate through subjects
            for key in main_dict[sub]:
                if key != "ANAT":
                    task = key
                    if not main_dict[sub][task]:
                        print("********************************EMPTY")
                    else:
                        with open(os.path.join(deriv_dir,'design.fsf'),'r') as infile:
                            tempfsf=infile.read()
                            out = main_dict[sub][task]["OUTPUT"]
                            func = main_dict[sub][task]["FUNCRUN"]
                            time = main_dict[sub][task]["NTIMEPOINT"]
                            con = main_dict[sub][task]["CONFOUND"]
                            anat = main_dict[sub]['ANAT']

                            print("----------------------> TASK: ", task)
                            print("----------------------> ANAT: ", anat)
                            print("----------------------> OUT: ", out)
                            print("----------------------> FUNC: ", func)
                            print("----------------------> TIME: ", time)
                            print("----------------------> CONFOUND: ", con)
                            tempfsf = tempfsf.replace("OUTPUT", out)
                            tempfsf = tempfsf.replace("FUNCRUN", func) #4D AVW DATA
                            tempfsf = tempfsf.replace("NTPTS", time)
                            tempfsf = tempfsf.replace("CONFOUND", con)
                            tempfsf = tempfsf.replace("ANAT", anat)
                            for i in range(8):
                                ev = main_dict[sub][task]["EV%i"%(i+1)]
                                n = i + 1
                                print("-----------> %s"%ev)
                                tempfsf = tempfsf.replace("EV%i"%n, ev)

                            for i in range(6):
                                moco = main_dict[sub][task]["MOCO%i"%i]
                                print("-------------------------> MOCO: ", moco)
                                tempfsf = tempfsf.replace("MOCO%i"%i, moco)
                            outpath= os.path.join(outdir, sub, arglist["SESS"], 'func', 'Analysis')
                            print("----------------------> OUTPATH: ", outpath)
                            if not os.path.exists(outpath):
                                os.makedirs(outpath)

                        with open(os.path.join(outpath,'%s_%s_task-%s_no_reg.fsf'%(sub,arglist["SESS"],task)),'w') as outfile:
                            outfile.write(tempfsf)
                        outfile.close()
                        infile.close()
                else:
                    pass




############################################################################################################
# FILL DICTIONARY METHOD
# here we are updating our dictionary with relevant values
############################################################################################################

def fill_dict(subj):
    #print("SUBJ: ", subj)
    for sub in main_dict:
        #print("------------------------> SUBJECT: ",sub)
            # -- OUTPUT -- directory where output will go
    # -- THE SUBEJCT
    #repl_dict.update({'SUB':sub})
        #deriv_dir = '/Users/nikkibytes/Documents/testing/derivatives'
    # -- THE RUNS
        data_dir = os.path.join(deriv_dir, sub, arglist["SESS"])


        #print("DATA DIRECTORY >>>>>> ", data_dir)
        #only getting milkshakes
        curr_funcs = glob.glob(os.path.join(data_dir, 'func', '*milkshake*bold_brain.nii.gz'))
        f = open(os.path.join(deriv_dir, "feat1_error_ses-2.txt"), "w")
        if not curr_funcs:
            print("EMPTY FUNC ----> ", sub)
            f.write(sub + "\n")
        for func in curr_funcs:
            words = func.split("/")[-1].split("_")
            for word in words:
                if 'task' in word:
                    task = word.split("-")[1]
                    fill_keys(task, sub)
            #print("TASK %s | SUB %s "%(task, sub))

            anat = os.path.join(data_dir, 'anat', 'highres001_BrainExtractionBrain.nii.gz')
            main_dict[sub]['ANAT'] = anat.split('.')[0]
            #print("ANAT >>>>>>>>>>>>>>>>> ", anat)

            output=os.path.join(data_dir, 'func', 'Analysis', 'feat1', 'task-%s'%task)
            main_dict[sub][task]['OUTPUT'] = output

            #print("OUTPUT >>>>>>>>>>>>>>>>>>> ", output)

            #split the func (must remove "nii.gz")
            #adds to dictionary
            funcrun = func.split('.')[0]
            main_dict[sub][task]["FUNCRUN"] =  funcrun
            #print("FUNCRUN \t >>>>>>>>>>>>>>>>>>> ", funcrun)

    # -- THE TIMEPOINTS -- found by running 'fslnvols' on our scan file
            ntmpts=check_output(['fslnvols', funcrun])
            ntmpts = ntmpts.decode('utf-8')
            ntmpts = ntmpts.strip('\n')
            main_dict[sub][task]['NTIMEPOINT'] = ntmpts
            #print("TIMEPOINT >>>>>>>>>>>>>>>>>>>", ntmpts)

    # -- CONFOUNDS
            confound=os.path.join(data_dir, 'func','motion_assessment','%s_%s_task-%s_bold_brain_confound.txt'%(sub,arglist["SESS"], task))
            main_dict[sub][task]['CONFOUND'] = confound
            #print("CONFOUNDS >>>>>>>>>>>>>>>>>>> ", confound)

    # -- MOTION CORRECTION
            for i in range(6):
                motcor=os.path.join(data_dir, 'func','motion_assessment', 'motion_parameters','%s_%s_task-%s_moco%s.txt' %(sub,arglist["SESS"],task,i))
                main_dict[sub][task]['MOCO%i'%i] = motcor
                #print("MOTCOR%i >>>>>>>>>>>>>>>>>>> %s "%(i,motcor))


    # -- EVS -- here we loop through the given EVs and add the corresponding file to the dictionary

            for ev_id in arglist['EV']:
            #print(item)
                #print("EV >>>>>>>>>> ", ev_id)
                mkID = task.split("e")[1]

                """
                h2O_receipt
                HF_HS_receipt
                HF_LS_receipt
                LS_HS_receipt
                LF_LS_receipt
                milkshake_pic
                h2O_pic
                rinse
                """


                if ev_id == "h2O_receipt":
                    ev=os.path.join(data_dir,'func','onsets','mk%s_h20_receipt.ev'%mkID)
                    #print("EV FILE >>>>>>>>>>>>>>> ", ev)
                    main_dict[sub][task]['EV1'] = ev
                elif ev_id == "HF_HS_receipt":
                    ev=os.path.join(data_dir,'func','onsets','mk%s_HF_HS_receipt.ev'%mkID)
                    #print("EV FILE >>>>>>>>>>>>>>> ", ev)
                    main_dict[sub][task]['EV2'] = ev
                elif ev_id == "HF_LS_receipt":
                    ev=os.path.join(data_dir,'func','onsets','mk%s_HF_LS_receipt.ev'%mkID)
                    #print("EV FILE >>>>>>>>>>>>>>> ", ev)
                    main_dict[sub][task]['EV3'] = ev
                if ev_id == "LF_HS_receipt":
                    ev=os.path.join(data_dir,'func','onsets','mk%s_LF_HS_receipt.ev'%mkID)
                    #print("EV FILE >>>>>>>>>>>>>>> ", ev)
                    main_dict[sub][task]['EV4'] = ev
                if ev_id == "LF_LS_receipt":
                    ev=os.path.join(data_dir,'func','onsets','mk%s_LF_LS_receipt.ev'%mkID)
                    #print("EV FILE >>>>>>>>>>>>>>> ", ev)
                    main_dict[sub][task]['EV5'] = ev
                if ev_id == "milkshake_pic":
                    ev=os.path.join(data_dir,'func','onsets','mk%s_milkshake_pic.ev'%mkID)
                    #print("EV FILE >>>>>>>>>>>>>>> ", ev)
                    main_dict[sub][task]['EV6'] = ev
                if ev_id == "h2O_pic":
                    ev=os.path.join(data_dir,'func','onsets','mk%s_h20_pic.ev'%mkID)
                    #print("EV FILE >>>>>>>>>>>>>>> ", ev)
                    main_dict[sub][task]['EV7'] = ev
                if ev_id == "rinse":
                    ev=os.path.join(data_dir,'func','onsets','mk%s_rinse.ev'%mkID)
                    #print("EV FILE >>>>>>>>>>>>>>> ", ev)
                    main_dict[sub][task]['EV8'] = ev
    f.close()



############################################################################################################
# CREATE FSF FILE
#
############################################################################################################.

def create_fsf():
    os.chdir(deriv_dir)
    global main_dict
    main_dict= {}
    for sub in glob.glob('sub-*'):
        print("SUBJECT: ", sub)
        set_dict(sub)
        fill_dict(sub)
        check_registartion(sub)

############################################################################################################
# MAIN METHOD
#
############################################################################################################.


def main():
    print("-----------------> BEGINNING PROGRAM")
    set_parser()
    if not arglist["SESS"]:
        print("SESSIONS list is empty")
    else:
        print("SETTING PATHS................")
        set_paths()
        create_fsf()
main()
