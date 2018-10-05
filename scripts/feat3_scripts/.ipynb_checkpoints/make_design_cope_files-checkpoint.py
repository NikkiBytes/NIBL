import glob
import os
from subprocess import check_output
import argparse
import re

def set_paths():
    global basedir
    global outdir
    global deriv_dir
    #basedir = input("Enter directory path of your data: ")
    #outdir = input("Enter directory path for your output: ")
    basedir='/projects/niblab/bids_projects/Experiments/bbx'
    deriv_dir=os.path.join(basedir, 'derivatives')
    outdir=os.path.join(deriv_dir)

def get_copes(x):
    COPES = glob.glob("/projects/niblab/bids_projects/Experiments/bbx/derivatives/sub-*/ses-1/func/Analysis/feat2/sub-*.gfeat/cope%s.feat"%x)
    COPES = sorted(COPES)
    return COPES 
def make_dict(x):
    cope_dict[x] = {}
    
def make_fsfs():
    template_file = "/projects/niblab/bids_projects/Experiments/bbx/derivatives/group_ana/group_ana.fsf"
    # get the number of cope files to make (# of copes)
    num_of_copes = 12
    num_of_input = 21
    # loop through copes and make design file for each
    for cope_num in range(1, num_of_copes+1):
        make_dict(cope_num)
        OUTPUTDIR = "/projects/niblab/bids_projects/Experiments/bbx/derivatives/group_ana/cope%s_ses-1"%cope_num
        print(">>>---> REPLACING 'OUTPUT' > %s"%OUTPUTDIR)
        COPES = glob.glob("/projects/niblab/bids_projects/Experiments/bbx/derivatives/sub-*/ses-1/func/Analysis/feat2/sub-*.gfeat/cope%s.feat"%cope_num)
        COPES = sorted(COPES)
        for x,cope in enumerate(COPES):
            count=int(x)+1
            if count > 9:
                INPUTX = "INPUT_%i"%(count)
            else: 
                INPUTX = "INPUT%i"%(count)
            cope_dict[cope_num][INPUTX] = cope
        with open(template_file, 'r') as infile:
            tempfsf=infile.read()
            tempfsf = tempfsf.replace("OUTPUT", OUTPUTDIR)
            for input_title in sorted(cope_dict[cope_num]):
                input_ = cope_dict[cope_num][input_title]
                print(">>>---> REPLACING ", input_title)
                tempfsf = tempfsf.replace("%s"%input_title, input_)
            OUTFILE_PATH = "/projects/niblab/bids_projects/Experiments/bbx/derivatives/group_ana/cope%s_ses-1.fsf"%cope_num
            print(tempfsf)
            with open(OUTFILE_PATH, 'w') as outfile:
                outfile.write(tempfsf)
            outfile.close()
        infile.close()

        
global COPES    
cope_dict = {}
set_paths()
make_fsfs()