import glob
import os
path = "/Users/nikkibytes/Documents/testing/Bevel/onsets/etc"
files = glob.glob(os.path.join(path, '*.txt'))


for onset in files:
    orig_name = onset.split('/')[8]
    print(orig_name)
    subID = orig_name.split('_')[0].split('l')[1]
    #print(subID)
    task = orig_name.split('_')[1]
    #print(task)
    run = orig_name.split('_')[2].split('0')[1].split('.')[0]
    #print(run)
    new_name = "sub-0%s_task-%s_run-%s.txt"%(subID, task, run)
    print(new_name)
