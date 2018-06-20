#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 17:05:35 2018

@author: nikkibytes
"""

import glob
import os
from subprocess import check_output
#import pdb
import argparse


def set_parser():
    global parser
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
    



def set_dict(sub):
    
    main_dict[sub] = {
            'SUB': None,
            'FUNCRUN': None,
            #'NTIMEPOINTS': None,
            'TR': None,
            #'OUTPUT': None,
            'ANAT': None,
            #'CONFOUNDS': None,
         }

############################################################################################################
# FILL DICTIONARY METHOD                            
# here we are updating our dictionary with relevant values
############################################################################################################
    
def fill_dict( ):
   
    for sub in main_dict:
        print(sub)
        
    # -- THE SUBEJCT 
    #repl_dict.update({'SUB':sub})
        deriv_dir = '/Users/nikkibytes/Documents/Test/derivatives'
    # -- THE RUNS
        for run in arglist['RUN']:
            scan=(os.path.join( sub,'func','%s_task-%s_run-%s_bold_brain.nii.gz')%(sub,arglist['TASK'], run))
            funcrun=os.path.join(deriv_dir, scan)
            x=int(run)
        #repl_dict.update({'FUNCRUN%i'%x:funcrun})
            print("FUNCRUN: ", funcrun)
        
    # -- THE TIMEPOINTS -- found by running 'fslnvols' on our scan file
            ntmpts=check_output(['fslnvols', funcrun])
            ntmpts = ntmpts.decode('utf-8')
            ntmpts = ntmpts.strip('\n')
       # repl_dict.update({'NTIMEPOINTS%i'%x:ntmpts})
            print("TIMEPOINT: ", ntmpts)

    # -- CONFOUNDS 
            confounds=os.path.join(deriv_dir,sub,'func','motion_assessment','%s_task-%s_run-%s_bold_brain_confound.txt'%(sub,arglist['TASK'],x))
      #  repl_dict.update({'CONFOUNDS%i'%x:confounds})
            print("CONFOUNDS: ", confounds)
        
    # -- MOTION CORRECTION
            for i in range(6):
                motcor=os.path.join(sub,'func','motion_assessment', 'motion_parameters','%s_task-%s_run-%s_moco%s.txt' %(sub,arglist['TASK'],run,i))
     #       repl_dict.update({'MOTCOR%i'%i:motcor})
                print("MOTCOR: ", motcor)


    # -- TRS FROM NIFTI -- this value will always be 2, therefore we only run the check once
        trs=check_output(['fslval','%s'%(funcrun),'pixdim4',scan])
        trs=trs.decode('utf-8')
        trs=trs.strip('\n')
        print("TRs: ", trs)
    #repl_dict.update({'TR':trs})
    
    
    # -- OUTPUT -- directory where output will go
        output=os.path.join(deriv_dir, sub, 'func', 'Analysis', 'task', arglist['TASK'])
    #repl_dict.update({'OUTPUT':output})
        print("OUTPUT: ", output)   
    
    
    # -- ANAT -- get the anat file for the subject, the syntax currently follows fmriprep standard
        anat=os.path.join(deriv_dir ,sub,'anat','highres001_BrainExtractionBrain.nii.gz')
    #repl_dict.update({'ANAT':anat})
        print("ANAT: ", anat)


    # -- EVS -- here we loop through the given EVs and add the corresponding file to the dictionary

        ctr=0
        for item in arglist['EV']:
            #print(item)
            ctr=ctr+1
            #repl_dict.update({'EV%iTITLE'%ctr:item})
            ev=os.path.join(sub,'func','onsets','%s_%s_%s_output.txt'%(sub,arglist['TASK'],item))
            print("EV: ", ev)
            #repl_dict.update({'EV%i'%ctr:ev})
        


global main_dict
main_dict = {}


set_dict('sub-001')

set_parser()
fill_dict()

#print("ARGLIST: ", arglist)
