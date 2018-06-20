
# coding: utf-8

# In[8]:


import pandas as pd
import os
import glob


# In[17]:


# get the data / directory
def get_subjects():
    global subjects
    global basedir
    subjects = []
    basedir=input("Enter the main directory: ")
    fmriprep_dir=os.path.join(basedir, 'fmriprep')
    os.chdir(fmriprep_dir)
    subjects=glob.glob("sub-*")


# In[18]:


def write_files(task, run, moco_df, outputdir, sub):
    for col in moco_df.columns:
        if task != 'task-rest':
            filename = "%s_%s_%s_%s.txt"%(sub, task, run, col)
        else:
            filename = "%s_task-rest.txt"%(sub)
        output_path=os.path.join(outputdir, filename)
        print("Writing to file, ", output_path)
        moco_df[col].to_csv(output_path, header=False, index=False)


# In[19]:


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


# In[20]:


def main():
    get_subjects()
    get_data()
    


# In[21]:


main()

