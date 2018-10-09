import glob
import os
from subprocess import check_output
import argparse
import re


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
    parser.add_argument('-sess ',dest='SESS',
                        default=False, help='which ses are we using?')
    parser.add_argument('-input_dir ',dest='INDIR',
                        default=False, help='please enter your input directory')
    parser.add_argument('-deriv_dir ',dest='DERIVDIR',
                        default=False, help='please enter your derivatives directory')
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]

        
def set_paths():
    global input_dir
    global deriv_dir
    global data_dir
    input_dir = arglist["INDIR"]
    deriv_dir = arglist["DERIVDIR"]
    if arglist["MULTI_SESS"] == True:
        data_dir = os.path.join(deriv_dir, sub, arglist["SESS"])
    else:
        data_dir = os.path.join(deriv_dir, sub)
    
# SET DICTIONARY METHOD FOR NO RUNS
def set_dict(sub):
    main_dict[sub] = {} 
    
# SET DICTIONARY METHOD FOR NO RUNS 
def set_run_dict(sub):
    main_dict[sub] = {}
    for run in arglist["RUN"]:
        main_dict[sub][run] = {}
        
def fill_dict(subj):

def fill_run_dict(subj):
        
            
def create_fsf():
    global main_dict
    main_dict= {}
    # RETREIVE SUBJECTS FROM INPUT DIRECTORY AND LOOP THROUGH SUBJECT TO FILL DICTIONARY
    for sub in glob.glob(os.path.join(input_dir, 'sub-*')):
        # CHECK FOR MULTIPLE RUNS -- GO TO RELEVANT METHOD FOR CONDITION 
        # 1ST CONDITION IS NO RUNS
        if not arglist["RUN"]:
            set_dict(sub)
            fill_dict(sub)
        # 2ND CONDITION IS RUNS 
        else:
            set_run_dict(sub)
            fill_run_dict(sub)