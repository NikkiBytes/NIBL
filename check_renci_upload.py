"""
Make a data listener for incoming data from OSIRIX
To start we will make a program that documents the current subjects in the directory
"""
import glob
import os

# Get the data path

#path=input("ENTER THE DATA PATH: ")
path="/projects/niblab/bids_projects/raw_data/continuing_studies/BRO"
keyword = "*0*"
glob_path=os.path.join(path, keyword)
dir_contents=glob.glob(glob_path)
filename = os.path.join(path, "%s_on_RENCI.txt"%(path.split("/")[-1]))
subjects=[]
os.remove(filename)
for subj_dir in dir_contents:
    subj = subj_dir.split("/")[-1]
    subjects.append(subj)
subjects = sorted(subjects)
outfile = open(filename, 'w')
for sub in subjects:
    print("WE ARE WRITING TO FILE NOW----------------------> ", sub)
    outfile.write(sub + "\n")
outfile.close()
