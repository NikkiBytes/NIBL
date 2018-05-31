# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import glob
import os
import pdb
import subprocess
import argparse
import datetime
import shutil
import os
#num_scrub = #some number that is ~25% of TRS

def preproc(DATA):
    print("Starting motion correction ")
    basedir='/Users/nikkibytes/Documents/testing'
    writedir='/Users/nikkibytes/Documents/testing/sub-001/fmriprep/sub-001/func/motion_assessment'
    
    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    outhtml = os.path.join(writedir,'bold_motion_QA_test_%s.html'%(datestamp))
    out_bad_bold_list = os.path.join(writedir,'testing_%s.txt'%(datestamp))
    print("OUTPUT HTML: ", outhtml )
    for sub in DATA:
        print("SUBJECT: ", sub)
        for dir in glob.glob(os.path.join(sub,'fmriprep/sub-001/func')):#path to the functional, skull stripped data
            print("DIRECTORY: ", dir)#not needed but i get crazy 
           
                
            os.path.join(dir)
            if not os.path.exists(os.path.join(dir,'motion_assessment')): #looking for a motion assessment dir to put out put in, I like to put it in my functional directory where my skull stripped brain is
                os.makedirs(os.path.join(dir,'motion_assessment')) #making dir if it doesn't exist
            for input in glob.glob(os.path.join('*brainmask.nii.gz')):
                id=input.split('.')[0]
                new_input=os.path.join(dir, id)
                cmd="fslnvols " + input
                print("CMD:", cmd)
                comparator = subprocess.check_output(cmd, shell=True, encoding="utf-8")
                comparator = comparator.strip()
                comparator = int(comparator) *.25
                print("Comparison: ", comparator)
                output=os.path.join(dir, 'motion_assesment/'+id+'_confound.txt ')
                print("INPUT: ", new_input)
                print("OUTPUT: ", output)
                # this is generating the fd confounds txt, it is using the fd metric,
                # making a plot and putting it in the motion assessment directory we made above

                os.system("fsl_motion_outliers -i %s -o %s --nomoco  --fd --thresh=0 -p motion_assessment/fd_plot -v > %s_outlier_output.txt"%(new_input,output,output))
                
            
                
                
                ####this is writing the motion assessment fd metric to the html file
                os.system("cat motion_assessment/%s_outlier_output.txt >> %s"%(id,outhtml))
                
                ###getting the full path to the plot
                plotz=os.path.join(basedir,dir,'motion_assessment','fd_plot.png')
                
                
                #### putting the full plot in the html file
                os.system("echo '<p>=============<p>FD plot %s <br><IMG BORDER=0 SRC=%s WIDTH=%s></BODY></HTML>' >> %s"%(id,plotz,'100%', outhtml))
                
                
                ####sometimes you have a great subject who didn't move, in this case we want to make a blank file
                if os.path.isfile("motion_assessment/%s_confound.txt"%(id))==False:
                    os.system("touch motion_assessment/%s_confound.txt"%(id))
            
                check = subprocess.check_output("grep -o 1 motion_assessment/%s_confound.txt | wc -l"%(id), shell=True) #how many columns are there = how many 'bad' points
                num_scrub = [int(s) for s in check.split() if s.isdigit()]

             
                if num_scrub[0] > comparator: #if the number in check is greater than num_scrub then we don't want it
                    with open(out_bad_bold_list, "a") as myfile: #making a file that lists all the bad ones
                        myfile.write("%s\n"%(id))
                        print("wrote bad file")
                    myfile.close()
def main(DATA):
    

    #parser=argparse.ArgumentParser(description='preprocessing')
   # parser.add_argument('--moco', type=float, help='this is using fsl_motion_outliers to preform motion correction and generate a confounds.txt as well as DVARS')
    #args = parser.parse_args('--moco', '0.9')
  #  args.const
    #arglist={}
    #for a in args._get_kwargs():
     #   arglist[a[0]]=a[1]
      #  print(a)
    #print(arglist['MOCO'])
    preproc(all_data)

all_data=glob.glob('/Users/nikkibytes/Documents/testing/sub*')
all_data
main(all_data)
