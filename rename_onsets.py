import glob
import os
path = "/Users/nikkibytes/Documents/testing/BIDS"
bevel_txt = "/Users/nikkibytes/Documents/testing/Bevel/Bevel.txt"


# Dictionary 

def getConversionDict():
    global conversion
    conversion = {}
    with open(bevel_txt, 'r') as f:
        for line in f:
            newsub = line.split("\t")[0].strip(' ')
            origsub = line.split("\t")[1].split("_")[0].split('l')[1]
            conversion[newsub] = origsub



def parseFile():
    os.chdir(path)
    subs = glob.glob('sub-*')
    print(subs)
    for dir_ in subs:
        curr_sub = dir_
        
        fmaps = glob.glob(os.path.join(dir_,'fmap', 'sub-*'))
        funcs = glob.glob(os.path.join(dir_,'func', 'sub-*'))
        anats = glob.glob(os.path.join(dir_,'anat', 'sub-*'))
        
        
        for file in fmaps:
            print(file)
        
        #for file in fmaps:
         #   orgname = 
        print(fmaps)
        print("________________________________________")
        print(funcs)
        print("________________________________________")
        print(anats)
        
    '''for onset in files:
        orig_name = onset.split('/')[8]
        print("ORIGINAL: ", orig_name)
        orig_ID = orig_name.split('_')[0].split('l')[1]
    #print(orig_ID)
        newID = conversion[orig_ID]
        #print(newID)
        task = orig_name.split('_')[1]
    #print(task)
        run = orig_name.split('_')[2].split('0')[1].split('.')[0]
        #print(run)
        new_name = "%s_task-%s_run-%s.txt"%(newID, task, run)
        print("NEW: ", new_name)
        '''
getConversionDict()
parseFile()
conversion