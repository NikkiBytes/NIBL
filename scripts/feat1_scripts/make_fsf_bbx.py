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
    basedir='/projects/niblab/bids_projects/Experiments/bbx'
    deriv_dir=os.path.join(basedir, 'derivatives')
    outdir=os.path.join(deriv_dir)

############################################################################################################
# SET DICTIONARY METHOD
# here we are passed our subject parameter and we initialize our dictionary key, the subject,
# and fill it with another dictionary set with starting values.
############################################################################################################

def set_dict(sub):
    main_dict[sub] = { }
    for run in arglist["RUN"]:
        main_dict[sub][run] = {}


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
        print("skipping registration......")
        for key in main_dict: #iterate through subjects
            for run in arglist["RUN"]: #iterate through runs
                with open(os.path.join(deriv_dir,'design_files/design1.fsf'),'r') as infile:
                    tempfsf=infile.read()
                    num=int(run)
                    out = main_dict[key][run]["OUTPUT"]
                    func = main_dict[key][run]["FUNCRUN"]
                    time = main_dict[key][run]["NTIMEPOINT"]
                    con = main_dict[key][run]["CONFOUND"]

                    print("----------------------> RUN: ", run)
                    print("----------------------> OUT: ", out)
                    print("----------------------> FUNC: ", func)
                    print("----------------------> TIME: ", time)
                    print("----------------------> CONFOUND: ", con)


                    tempfsf = tempfsf.replace("OUTPUT", out)
                    tempfsf = tempfsf.replace("FUNCRUN", func) #4D AVW DATA
                    tempfsf = tempfsf.replace("NTPTS", time)
                    tempfsf = tempfsf.replace("CONFOUND", con)

                    for key2 in main_dict[key][run]:
                        if re.match(r'EV[0-9]TITLE', key2):
                            ev_title = main_dict[key][run][key2]
                            n = re.findall('\d+', key2)
                            n = ''.join(str(x) for x in n)
                            ev = main_dict[key][run]["EV%s"%n]
                            print("----------------------> EVTITLE: ", ev_title)
                            print("-----------> EV%s"%n, ev)
                            #tempfsf = tempfsf.replace("EV%sTITLE"%n, ev_title)
                            tempfsf = tempfsf.replace("EV%s"%n, ev)

                    for i in range(6):
                        moco = main_dict[key][run]["MOCO%i"%i]
                        tempfsf = tempfsf.replace("MOCO%i"%i, moco)
                        print("----------------------> MOCO%i: "%i , main_dict[key][run]["MOCO%i"%i])
                    outpath= os.path.join(outdir, sub, arglist["SESS"], 'func', 'Analysis')
                    print("----------------------> OUTPATH: ", outpath)
                    if not os.path.exists(outpath):
                        os.makedirs(outpath)

                    print("__________________________________________________________")
                    #print(tempfsf)
                    print("__________________________________________________________")

                #print(main_dict[key])
                    with open(os.path.join(outpath,'%s_%s_task-%s_run-%s_no_reg.fsf'%(sub,arglist["SESS"],arglist['TASK'], run)),'w') as outfile:
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
        print("------------------------> SUBJECT: ",sub)
            # -- OUTPUT -- directory where output will go
    # -- THE SUBEJCT
    #repl_dict.update({'SUB':sub})
        #deriv_dir = '/Users/nikkibytes/Documents/testing/derivatives'
    # -- THE RUNS
        if arglist["MULTI_SESS"] == True:
            data_dir = os.path.join(deriv_dir, sub, arglist["SESS"])
        else:
            data_dir = os.path.join(deriv_dir, sub)

        print("DATA DIRECTORY >>>>>> ", data_dir)

        for run in arglist["RUN"]:
            x=int(run)
            print("RUN: ", run)
            output=os.path.join(data_dir, 'func', 'Analysis', 'feat1', 'task-%s_run%s'%(arglist["TASK"],run))
            main_dict[sub][run]['OUTPUT'] = output
            print("OUTPUT >>>>>>>>>>>>>>>>>>> ", output)

        #sub-015_ses-1_task-training_run-1_bold_brain.nii.gz
        #sub-016_ses-1_task-training_run-2_bold_brain_confound.txt
            if arglist["MULTI_SESS"] == True:
                func_scan = os.path.join(data_dir, 'func', "%s_%s_task-%s_run-%s_bold_space-MNI152NLin2009cAsym_preproc_brain.nii.gz.nii.gz')"%(sub,arglist['SESS'], arglist['TASK'], run))
                confounds=os.path.join(data_dir, 'func','motion_assessment','%s_%s_task-%s_run-%s_bold_space-MNI152NLin2009cAsym_preproc_brain_confound.txt'%(sub,arglist["SESS"],arglist['TASK'], run))
            else:
                func_scan = os.path.join(data_dir,'func', "%s_task-%s_run-%s_bold_brain.nii.gz')"%(sub,arglist['TASK'], run))
                confounds=os.path.join(data_dir,'func','motion_assessment','%s_task-%s_run-%s_bold_space-MNI152NLin2009cAsym_preproc_brain_confound.txt'%(sub,arglist['TASK'],x))
            scan= func_scan
            funcrun = scan.split('.')[0]
            funcrun=os.path.join(funcrun)
            main_dict[sub][run]['FUNCRUN'] =  funcrun
            print("FUNCRUN \t >>>>>>>>>>>>>>>>>>> ", funcrun)

    # -- THE TIMEPOINTS -- found by running 'fslnvols' on our scan file
            ntmpts=check_output(['fslnvols', funcrun])
            ntmpts = ntmpts.decode('utf-8')
            ntmpts = ntmpts.strip('\n')
            main_dict[sub][run]['NTIMEPOINT'] = ntmpts
            print("TIMEPOINT >>>>>>>>>>>>>>>>>>>", ntmpts)

    # -- CONFOUNDS
            main_dict[sub][run]['CONFOUND'] = confounds
            print("CONFOUNDS >>>>>>>>>>>>>>>>>>> ", confounds)

    # -- MOTION CORRECTION
            for i in range(6):
                motcor=os.path.join(data_dir, 'func','motion_assessment', 'motion_parameters','%s_%s_task-%s_run-%s_moco%s.txt' %(sub,arglist["SESS"],arglist['TASK'],run,i))
                main_dict[sub][run]['MOCO%i'%i] = motcor
                print("MOTCOR%i >>>>>>>>>>>>>>>>>>> %s "%(i,motcor))


    # -- TRS FROM NIFTI -- this value will always be 2, therefore we only run the check once
            trs=check_output(['fslval','%s'%(funcrun),'pixdim4',scan])
            trs=trs.decode('utf-8')
            trs=trs.strip('\n')
            print("TRs: ", trs)
            main_dict[sub][run]['TR'] = trs



    # -- EVS -- here we loop through the given EVs and add the corresponding file to the dictionary

            ctr=0
            for ev_id in arglist['EV']:
            #print(item)
                print("EV >>>>>>>>>> ", ev_id)

                ctr=ctr+1
                #loop through the arglist["EV"] titles and add corresponding title/file to dictionary
                #here we are adding the EV Title
                main_dict[sub][run]['EV%iTITLE'%ctr] = ev_id
                ev=os.path.join(data_dir,'func','onsets','%s_%s_task-%s_run-0%s.txt'%(sub,arglist["SESS"], ev_id,run))
                #ev=os.path.join(data_dir,'func','onsets','%s_task-%s_run-%s.txt'%(sub,item,run))
                print("EV FILE >>>>>>>>>>>>>>> ", ev)
                main_dict[sub][run]['EV%i'%ctr] = ev


############################################################################################################
# CREATE FSF FILE
#
############################################################################################################.

def create_fsf():
    os.chdir(deriv_dir)
    global main_dict
    main_dict= {}
    for sub in glob.glob('sub-*'):
        print(sub)
        set_dict(sub)
        fill_dict(sub)
        #print(main_dict)
        #print(main_dict[sub]["4"])
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
        #print(main_dict["sub-001"]["1"])
main()
