import glob
import os
import argparse



path = '/projects/niblab/bids_projects/Experiments/EricData/data'
derivpath= os.path.join(path, 'derivatives')
bevel_txt = os.path.join(path, 'Bevel.txt')
print(derivpath)



#path = "/projects/niblab/bids_projects/Experiments/Bevel/data/Bevel"
#bevel_txt = "/projects/niblab/bids_projects/Experiments/Bevel/data/Bevel.txt"






def set_parser():

    global arglist

    parser=argparse.ArgumentParser(description='make your fsf files')
    parser.add_argument('-bids',dest='BIDS', action='store_true',
                        default=False, help='rename BIDS?')
    parser.add_argument('-deriv',dest='DERIV', action='store_true',
                        default=False, help='rename derivatives?')

    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]

# Dictionary

def getConversionDict():
    global conversion

    conversion = {}
    with open(bevel_txt, 'r') as f:
        for line in f:
            newsub = line.split("\t")[0].strip(' ')
            origsub = line.split("\t")[1].split("_")[0].split('l')[1]
            conversion[newsub] = origsub



def renameBIDS():
    os.chdir(path)
    subs = glob.glob('sub-*')

    # replace individual files
    for dir_ in subs:
        print(dir_)
        curr_sub = dir_
        new_sub = "sub-0"+conversion[curr_sub]

        #print(curr_sub, new_sub)

        os.chdir(os.path.join(path,dir_,'fmap'))
        fmaps = glob.glob('sub-*')

        for file in fmaps:
            #print("ORIGINAL", file)
            new = file.replace(curr_sub, new_sub)
            print("ORIGINAL FMAP:", file)
            print("NEW FMAP: ", new)
            os.replace(file, new)


        os.chdir(os.path.join(path,dir_,'func'))
        funcs = glob.glob('sub-*')

        for file in funcs:
            new = file.replace(curr_sub, new_sub)
            print("ORIGINAL FUNC:", file)
            print("NEW FUNC:", new)
            os.replace(file, new)


        os.chdir(os.path.join(path,dir_,'anat'))
        anats = glob.glob('sub-*')

        for file in anats:
            new = file.replace(curr_sub, new_sub)
            print("ORIGINAL ANAT: ", file)
            print("NEW ANAT: ", new)
            os.replace(file, new)


        os.chdir(os.path.join(path, dir_))
        subdir = glob.glob("*%s*"%dir_)
        for file in subdir:
            new = file.replace(curr_sub, new_sub)
            print(file)
            print(new)
            os.replace(file, new)

def renameDir(input_path):

    os.chdir(input_path)

    subs = glob.glob('sub-*')
    for dir_ in subs:
        curr_sub = dir_
        new_sub = "sub-0"+conversion[curr_sub]
        os.replace(dir_, new_sub)

def renameDeriv():
    os.chdir(derivpath)
    subs = glob.glob('sub-*')


    for dir_ in subs:
        print(dir_)
        curr_sub = dir_
        new_sub = "sub-0"+conversion[curr_sub]

        os.chdir(os.path.join(derivpath,dir_, 'func'))
        funcs = glob.glob("*%s*"%dir_)

        for file in funcs:
            print(file)
            new = file.replace(curr_sub, new_sub)
            print("-------> ",new)
            os.replace(file, new)

        os.chdir('motion_assessment')
        confounds = glob.glob("*%s*"%dir_)

        for file in confounds:
            print(file)
            new = file.replace(curr_sub, new_sub)
            print("-------> ",new)
            os.replace(file, new)


        os.chdir('motion_parameters')
        mocos = glob.glob("*%s*"%dir_)

        for file in mocos:
            print(file)
            new = file.replace(curr_sub, new_sub)
            print("-------> ",new)
            os.replace(file, new)




set_parser()
getConversionDict()

if arglist["BIDS"] == True:
    print("here")
    renameBIDS()
    renameDir()

if arglist["DERIV"] == True:
    print('here in deriv')
    renameDeriv()
    renameDir(derivpath)
