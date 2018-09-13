#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 20:26:22 2018

@author: nikkibytes
"""
import glob
import os
import shutil

path = "/projects/niblab/bids_projects/Experiments/Bevel/data"
derivpath = os.path.join(path, 'derivatives')
onsetpath = os.path.join(path, 'onsets')

print(onsetpath)
os.chdir(derivpath)

subjects = glob.glob("sub-*")
onsets = glob.glob(os.path.join(onsetpath,"*.txt"))
#print(onsets)
for dir_ in subjects:
    sub = dir_
    new_dest = os.path.join(derivpath, sub, "func", "onsets")
    if not os.path.exists(new_dest):
        os.makedirs(new_dest) 
    #print(sub_dir)
    #print(sub)
    for onset in onsets:
        if sub in onset:
            try:
                curr_dest = onset
            
                print(onset)
                print("________________________________")
            
                shutil.move(curr_dest, new_dest)
            except FileNotFoundError:
                pass 
    
#for  in onsets:
 #       print(onset)