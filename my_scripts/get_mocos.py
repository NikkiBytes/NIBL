
# coding: utf-8
"""
@author: Nichollette Acosta, NIBL UNC Chapel Hill
This scripts creates the 1-column motion correction (.txt) files
The only input required is the directory path that holds the fmriprep directory
and derivative directory
"""




import pandas as pd
import os
import glob



'''
 The get_subjects() method takes the input from the user,
 and sets a basedir variable holding the input path,
 it sets the fmriprep_dir based on the basedir,
 and it goes to the fmriprep directory and gathers a list of subjects
'''
def get_subjects():
    global subjects
    global basedir
    subjects = []
    basedir=input("Enter the main directory: ")
    fmriprep_dir=os.path.join(basedir, 'fmriprep')
    os.chdir(fmriprep_dir)
    subjects=glob.glob("sub-*")




'''
 The write_files() method takes in various variables,
 the task label, the run #, the subject(sub), the output directory(outputdir),
 and then the motion correction dataframe holding the relevant data,
 and writes the data into a (.txt) file
'''
def write_files(task, run, moco_df, outputdir, sub):
    for col in moco_df.columns:
        if task != 'task-rest':
            filename = "%s_%s_%s_%s.txt"%(sub, task, run, col)
        else:
            filename = "%s_task-rest.txt"%(sub)
        output_path=os.path.join(outputdir, filename)
        print("Writing to file, ", output_path)
        moco_df[col].to_csv(output_path, header=False, index=False)



'''
 The get_data() method iterates through the subjects (gathered in the get_subjects method),
 and sets the file path (the fmriprep func path that holds the *confound.tsv files),
 then it sets the output directory, (the derivatives folder, it  creates the 'motion_parameters'
 directory if it is not there), then the program moves to the filepath directory and iterates through
 the confound files and pulls out the the relevant data (the motion corrected columns). Finally
 the program calls the write_files() method and writes the data to the file.
'''
def get_data():
    for sub in subjects:
        #print(sub)
        filepath=os.path.join(basedir, 'fmriprep', sub, 'fmriprep', sub, 'func')
        outputdir=os.path.join(basedir, 'derivatives', sub, 'func', 'motion_assessment')
        if not os.path.exists(os.path.join(outputdir, 'motion_parameters')):
            os.makedirs(os.path.join(outputdir,  'motion_parameters'))
        outputdir=os.path.join(outputdir, 'motion_parameters')
        os.chdir(filepath)
        for run in glob.glob("*confounds.tsv"):
       # print("FILE: ", run)
            df = pd.read_table(run)
            moco_df=df[['X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']]
            moco_df.columns = ['moco0', 'moco1', 'moco2', 'moco3', 'moco4', 'moco5']
        #print(moco_df.head())
            name=run.split('_')
    #    print(task)
            for word in name:
                if 'task' in word:
                    task=word
            if task == "task-rest":
                run=None
                write_files(task, run, moco_df, outputdir,sub)
            else:
                for word in name:
                    if 'run' in word:
                        run=word
                write_files(task, run, moco_df,outputdir,sub)
#        print("TASK: ", task)
#        print("RUN: ", run)


'''
 The main() method is the first to execute, it first calls the get_subject method,
 then it calls our get_data() method.
'''
def main():
    get_subjects()
    get_data()

main()