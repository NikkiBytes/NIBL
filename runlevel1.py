#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 12:21:50 2018

@author: nikkibytes
"""

import os 
import glob
from multiprocessing import Pool 



basedir='/Users/gracer/Desktop/data/derivatives/task'
all_data=glob.glob(os.path.join(basedir,'sub*','sub*bart.fsf'))
def split_list(a_list):
        half = len(a_list)/2
        return a_list[:half], a_list[half:]

B, C = split_list(all_data)

def run_level1(DATA):
    for item in DATA:
        print('starting to run on %s'%item)
        os.system("feat %s"%item)    

if __name__ == '__main__':
   pool = Pool(processes=2)
   pool.map(run_level1, [B,C])
   pool.close()
   pool.join()
   