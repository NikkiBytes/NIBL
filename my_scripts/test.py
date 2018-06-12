import glob
import os
import subprocess
import datetime
import argparse

def set_parser():
    global parser
    global arglist
    global args
    parser=argparse.ArgumentParser(description='preprocessing')

    parser.add_argument('-task',dest='TASK',
                        default=False, help='which task are we running on?')
    parser.add_argument('-moco',dest='MOCO',
                        action="store_true", help='this is using fsl_motion_outliers to preform motion correction and generate a confounds.txt as well as DVARS')
    parser.add_argument('-bet',dest='STRIP',action='store_true',
                        default=False, help='bet via fsl using defaults for functional images')


    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
    print(arglist)



def preproc(DATA):
    if args.MOCO==False:
        print("please set a threshold for the FD, a good one is 0.9")
    else:
        print("starting motion correction")

    if args.STRIP==True:
        print("starting bet")
        print("PRINTING DATA: \n", DATA. "\n")
        #os.chdir(os.path.join(basedir))
        for sub in DATA:
            for nifti in glob.glob(os.path.join(sub, 'func', 'sub-*_task-%s_bold.nii.gz')%(arglist['TASK'])):
                # make our variables
                output=nifti.strip('.nii.gz')
                BET_OUTPUT=output+'_brain'
                # check if data exists already
                if os.path.exists(BET_OUTPUT):
                    print(BET_OUTPUT + ' exists, skipping \n')
                else:
                    print("Running bet on ", nifti)
                    print("BET COMMAND: ", bet_cmd, "\n")
                    bet_cmd=("bet %s %s -F -m"%(nifti, BET_OUTPUT))
                #    os.system(bet_cmd)

        # lets check our variables
                print("VARIABLES:")
                print("SUB: ", sub)
                print("NIFTI: ", nifti)
                print("OUTPUT: ", output)
                print("BET OUTPUT: ", BET_OUTPUT)
                print("__________________________________________________________________________________")

def main():
        set_parser()
        sub_dir=glob.glob('/projects/niblab/bids_projects/Experiments/test/sub*')
        preproc(sub_dir)

main()
