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
    parser.add_argument('-run',dest='RUN',nargs='+',
                        default=False, help='which run are we using?')    
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
    



def set_dict():
    global repl_dict
    
    repl_dict = {
                'SUB': None,
                'FUNCRUN': None,
                'NTIMEPOINTS': None,
                'TRS': None,
                'OUTPUT': None,
                'ANAT': None,
                'CONFOUNDS': None,
         }


def fill_dict(sub):
    
    repl_dict.update({'SUB':sub})
    ctr=0
    for item in arglist['EV']:
        print(item)
        ctr=ctr+1
        repl_dict.update({'EV%iTITLE'%ctr:item})
        ev=os.path.join(sub,'func','onsets','%s_%s_%s_output.txt'%(sub,arglist['TASK'],item))
        print(ev)
        repl_dict.update({'EV%i'%ctr:ev})
        for i in range(6):
            motcor=os.path.join(sub,'func','motion_assessment','%s_task-%s_bold_brain_motcor%i.txt' %(sub,arglist['TASK'],i))
            repl_dict.update({'MOTCOR%i'%i:motcor})
    # FUNCRUN --
   # scan=(os.path.join('derivatives', sub,'func','%s_task-%s_run-%s_bold_brain.nii.gz')%(sub,arglist['TASK'], arglist['RUN']))
    #print(scan)
    #funcrun = os.path.join(deriv_dir, sub, scan)
    #repl_dict.update({'FUNCRUN':funcrun})
    

set_dict()
set_parser()
fill_dict('sub-001')

#print("ARGLIST: ", arglist)
print("DICT: ", repl_dict)