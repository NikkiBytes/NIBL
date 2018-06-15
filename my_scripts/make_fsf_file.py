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


def set_parser():
  global parser

  parser=argparse.ArgumentParser(description='make your fsf files')
  parser.add_argument('-noreg',dest='NOREG', action='store_true',
                        default=False, help='Did you already register your data (using ANTZ maybe)?')
  parser.add_argument('-task',dest='TASK',
                        default=False, help='which task are we using?')
  parser.add_argument('-evs',dest='EV',nargs='+',
                        default=False, help='which evs are we using?')
  args = parser.parse_args()
  arglist={}
  for a in args._get_kwargs():
      arglist[a[0]]=a[1]
      print(arglist)

def set_paths():
    global basedir
    global outdir
    #basedir = input("Enter directory path of your subjects: ")
    #outdir = input("Enter directory path for your output: ")
    basedir='/Users/gracer/Desktop/data'
    outdir=os.path.join(basedir,'derivatives','task')

def set_dict():
    global repl_dict
    os.chdir(basedir)
    repl_dict = {
                'SUB': None,
                'FUNCRUN': None,
                'NTIMEPOINTS': None,
                'TRS': None,
                'OUTPUT': None,
                'ANAT': None,
                'CONFOUNDS': None, 
         }

    for sub in glob.glob('sub-*'):


def create_fsf():
    os.chdir(basedir)

def main():
    set_parser()

main()
