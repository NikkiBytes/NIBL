#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:21:50 2018

@author: nikkibytes
"""

import os
import glob
import psutil 
from multiprocessing import Pool



basedir='/projects/niblab/bids_projects/Experiments/EricData/data'
all_data=glob.glob(os.path.join(basedir, 'derivatives', 'sub*', 'ses-2', 'func', 'Analysis', 'sub*.fsf'))


def split_list(a_list):
        half = len(a_list)/2
        half = int(half)
        return a_list[:half], a_list[half:]

B, C = split_list(all_data)

def run_level1(DATA):
    try:
        for item in DATA:
            print('starting to run on %s'%item)
            os.system("feat %s"%item)
    except Exception:
        with open(basedir+"/bad_files_ses-2_feat1.txt", 'a') as f:
            f.write("Bad file: ", item)
            f.close()

if __name__ == '__main__':
   pool = Pool(processes=2)
   pool.map(run_level1, [B,C])
   pool.close()
   pool.join()
