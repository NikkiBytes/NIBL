import glob
import os
from subprocess import check_output
import argparse
import re

## SET THE PROGRAM PARSER TO GET RELEVANT VARIABLES FROM USER
## CURRENTLY WE NEED "derivatives/" directory, design template file, # of copes, # of subjects, multiple sessions parameter
def set_parser():
    global parser
    global arglist
    global args
    parser=argparse.ArgumentParser(description="make group analysis (feat 3) design files")
    parser.add_argument('-basedir',dest='BASEDIR', default=False, help='Enter the derivatives/ directory path')
    parser.add_argument('-template',dest='TEMPLATE', default=False, help="Enter the path for the template design file")
    parser.add_argument('-subs',dest='SUBS',default=0, help='how many subjects?')
    parser.add_argument('-copes',dest='COPES', default=0, help='how many contrasts?')
    parser.add_argument('-ses',dest='SES', default=False, help='have multiple sessions?')


    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]

         

# SET OUR RELEVANT PATHS
def set_paths():
    global deriv_dir
    deriv_dir = arglist["BASEDIR"]


def make_dict(x):
    cope_dict[x] = {}


def make_fsfs():
    deriv_dir = arglist["BASEDIR"]
    template_file = arglist["TEMPLATE"]
    # get the number of cope files to make (# of copes)
    num_of_copes = int(arglist["COPES"])
    num_of_input = int(arglist["SUBS"])
    print(num_of_copes)
    # loop through copes and make design file for each
    for cope_num in range(1, num_of_copes+1):
        make_dict(cope_num)
        #OUTPUTDIR = os.path.join(deriv_dir, 'group_ana/cope%s_ses-1'%cope_num)
        OUTPUTDIR = os.path.join(deriv_dir, 'group_ana/mean')

        print(">>>---> REPLACING 'OUTPUT' > %s"%OUTPUTDIR)
        if arglist["SES"] == False:
            print("NO SESSION")
            COPES = glob.glob(os.path.join(deriv_dir, "sub-*",'func/Analysis/feat2/sub-*.gfeat/cope%s.feat'%cope_num))

        else:
            sess = arglist["SES"]
            print("RUNNING ON SESSION ", sess )
            COPES = glob.glob(os.path.join(deriv_dir, "sub-*", sess,'func/Analysis/feat2/sub-*.gfeat/cope%s.feat'%cope_num))
        COPES = sorted(COPES)
        for x,cope in enumerate(COPES):
            count=int(x)+1
            if count > 9:
                INPUTX = "INPUT_%i"%(count)
            else:
                INPUTX = "INPUT%i"%(count)
            cope_dict[cope_num][INPUTX] = cope
            print("%s >>>>-----> %s"%(INPUTX,cope))
        with open(template_file, 'r') as infile:
            tempfsf=infile.read()
            tempfsf = tempfsf.replace("OUTPUT", OUTPUTDIR)
            for input_title in sorted(cope_dict[cope_num]):
                input_ = cope_dict[cope_num][input_title]
                tempfsf = tempfsf.replace("%s"%input_title, input_)
            if arglist["SES"] == False:
                OUTFILE_PATH = os.path.join(deriv_dir, 'group_ana/cope%s.fsf'%cope_num)
            else:
                OUTFILE_PATH = os.path.join(deriv_dir, 'group_ana/cope%s_%s.fsf'%(cope_num, arglist["SES"]))
            #print(tempfsf)
            with open(OUTFILE_PATH, 'w') as outfile:
                print("Writing output file >>>-----> ", OUTFILE_PATH)
                outfile.write(tempfsf)
            outfile.close()
        infile.close()

def main():
    global COPES
    global cope_dict
    cope_dict = {}
    set_parser()
    make_fsfs()

if __name__ == "__main__":
    main()
