
# coding: utf-8
"""
@author: Nichollette Acosta, NIBL UNC Chapel Hill
This scripts creates the 1-column motion correction (.txt) files
The only input required is the directory path that holds the fmriprep
directory and derivative directory
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
    #print("SUBJECTS: ", subjects)

'''
 The write_files() method takes in various variables,
 the task label, the run #, the subject(sub), the output directory(outputdir),
 and then the motion correction dataframe holding the relevant data,
 and writes the data into a (.txt) file
'''
def write_files(task, run, moco_df, outputdir, sub):
    # iterate through the motion correction data frame by columns, writing individual columns to individual files
    for col in moco_df.columns:
        if run != None:
            filename = "%s_%s_%s_%s_%s.txt"%(sub, "ses-1", task, run, col)
            print("WRITING TO FILE >>>>>>>>>>>>>>>>>>>>>>> %s"%filename)
        else:
            #filename = "%s_task-rest.txt"%(sub)
            filename = "%s_%s_%s_%s.txt"%(sub, "ses-1", task, col)
            print("WRITING TO FILE >>>>>>>>>>>>>>>>>>>>>>> %s"%filename)
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
    """
    #SPECIAL CASE FOR REST
    if task == "task-rest":
        run_id=None
        #write_files(task, run_id, moco_df, outputdir,sub)
        print(">>>>>>>>RUN: %s"%run)
    else:
        for word in name:
            if 'run' in word:
                run_id=word
            print(">>>>>>>>RUN: %s"%run)
        #write_files(task, run_id, moco_df,outputdir,sub)
    """
'''


def get_data():
    errors = []
    for sub in subjects:
        try:
            print("--------------> GETTING MOCOS FOR SUBJECT: ", sub)
            filepath=os.path.join(basedir, 'fmriprep', sub, "ses-1" ,'fmriprep', sub, "ses-1", 'func')
            outputdir=os.path.join(basedir, 'derivatives', sub, "ses-1", 'func', 'motion_assessment')
            if not os.path.exists(os.path.join(outputdir, 'motion_parameters')):
                os.makedirs(os.path.join(outputdir,  'motion_parameters'))
            outputdir=os.path.join(outputdir, 'motion_parameters')
            print(">>>>>>>FILEPATH: %s >>>>>>>>OUTPUT DIRECTORY: %s"%(filepath, outputdir))
            os.chdir(filepath)
            for run in glob.glob("*confounds.tsv"):
                print("---------------------------------------------> GRABBING NEW FILE:")
                print("FILE: ", run)
                df = pd.read_table(run)
                moco_df=df[['X', 'Y', 'Z', 'RotX', 'RotY', 'RotZ']]
                moco_df.columns = ['moco0', 'moco1', 'moco2', 'moco3', 'moco4', 'moco5']
                print("DATAFRAME: \n ", moco_df.head())
                name=run.split('_')
                #print("NAME: ", name)
                for word in name:
                    if 'task' in word:
                        task=word
                        print("TASK: ", task)
                        #run_id=None
                        if task == "task-resting":
                            run_id=None
                            write_files(task, run_id, moco_df, outputdir,sub)
                            print(">>>>>>>>RUN: %s"%run)
                        else:
                            for word in name:
                                if 'run' in word:
                                    run_id=word
                                    print(">>>>>>>>RUN: %s"%run)
                            write_files(task, run_id, moco_df,outputdir,sub)
                #write_files(task, run_id, moco_df, outputdir,sub)
                #print("RUN: ", run)
        except FileNotFoundError as not_found:
            print("********************FILE NOT FOUND: ", not_found.filename)
            if sub not in errors:
                errors.append(sub)
        #print("ERRORS ", errors)
        #print("ERRORS SORTED ", sorted(errors))
        errors = sorted(errors)
    for err in errors:
            #print("ERROR" + err)
        file = basedir+"/error_files_moco.txt"
        with open(file, 'a') as f:
            f.write("--------------------------------> FILE NOT FOUND FOR SUBJECT: " + err  + "\n")
            f.close()
'''
 The main() method is the first to execute, it first calls the get_subject method,
 then it calls our get_data() method.
'''
def main():
    get_subjects()
    get_data()
main()
