import glob
import os
from subprocess import check_output
import argparse
import re

#########################################################################################################
# SET PARSER
#
#########################################################################################################


def set_parser():
    global arglist
    parser=argparse.ArgumentParser(description='make your fsf files')
    parser.add_argument('-noreg',dest='NOREG', action='store_true',
                        default=False, help='Did you already register your data (using ANTZ maybe)?')
    parser.add_argument('-task',dest='TASK',
                        default=False, help='which functional task are we using?')
    parser.add_argument('-evs',dest='EV',nargs='+',
                        default=False, help='which evs are we using?')
    parser.add_argument('-runs',dest='RUN',nargs='+',
                        default=False, help='which run are we using?')
    parser.add_argument('-multisess',dest='MULTI_SESS', action='store_true',
                        default=False, help='Do you have multiple sessions? (True or False)')
    parser.add_argument('-sess ',dest='SESS',
                        default=False, help='which ses are we using?')
    parser.add_argument('-input_dir ',dest='INDIR',
                        default=False, help='please enter your input directory')
    parser.add_argument('-deriv_dir ',dest='DERIVDIR',
                        default=False, help='please enter your derivatives directory')
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
        
        
#########################################################################################################
# GET DIRECTORY PATHS
#
#########################################################################################################

def set_paths():
    global input_dir
    global deriv_dir
    print(">>>----> SETTING PATHS")
    input_dir = arglist["INDIR"]
    deriv_dir=arglist["DERIVDIR"]
    
    
#########################################################################################################
# SET DICTIONARY METHOD
# here we are passed our subject parameter and we initialize our dictionary key, the subject,
# and fill it with another dictionary set with starting values.
#########################################################################################################

def set_dict(sub):
    main_dict[sub] = { }
    if not arglist["RUN"]:
         pass
    else:
        for run in arglist["RUN"]:
            main_dict[sub][run] = {}
            
def make_file(sub):
    print("skipping registration")
    for key in main_dict:
        for run in arglist["RUN"]:
            with open(os.path.join(deriv_dir,'design1.fsf'),'r') as infile:
                tempfsf=infile.read()

                num=int(run)
                out = main_dict[key][run]["OUTPUT"]
                func = main_dict[key][run]["FUNCRUN%i"%num]
                time = main_dict[key][run]["NTIMEPOINT%i"%num]
                con = main_dict[key][run]["CONFOUND%i"%num]

                tempfsf = tempfsf.replace("OUTPUT", out)
                tempfsf = tempfsf.replace("FUNCRUN", func) #4D AVW DATA
                tempfsf = tempfsf.replace("NTPTS", time)
                tempfsf = tempfsf.replace("CONFOUND", con)

                for key2 in main_dict[key][run]:
                    if re.match(r'EV[0-9]TITLE', key2):
                        ev_title = main_dict[key][run][key2]
                        n = re.findall('\d+', key2)
                        n = ''.join(str(x) for x in n)
                        ev = main_dict[key][run]["EV%s"%n]
                        print("EVTITLE: ", ev_title)
                        print("EV%s"%n, ev)
                        #tempfsf = tempfsf.replace("EV%sTITLE"%n, ev_title)
                        tempfsf = tempfsf.replace("EV%s"%n, ev)

                for i in range(6):
                    moco = main_dict[key][run]["MOCO%i"%i]
                    tempfsf = tempfsf.replace("MOCO%i"%i, moco)
                    print("MOCO%i: "%i , main_dict[key][run]["MOCO%i"%i])
                outpath= os.path.join(deriv_dir, sub, 'func', 'Analysis', "feat1")
                #print(tempfsf)
                if not os.path.exists(outpath):
                    os.makedirs(outpath)
                print("OUT PATH >>>>>>---------> ", outpath)
                with open(os.path.join(outpath,'%s_task-%s_run-%s_no_reg.fsf'%(sub,arglist['TASK'], run)),'w') as outfile:
                    outfile.write(tempfsf)
                outfile.close()
            infile.close()
        
def fill_dict(sub):
    for sub in main_dict:
        task = arglist['TASK']
        print("SUBJECT: %s \t TASK: %s"%(sub, task))

    # -- THE RUNS
        data_dir = os.path.join(deriv_dir, sub)
        print("DATA DIR", data_dir)
        
        for run in arglist['RUN']:
            x=int(run)
            output=os.path.join(data_dir, 'func', 'Analysis', 'feat1', 'task-%s_run%s'%(task,run))
            func = os.path.join(deriv_dir, sub, 'func', "%s_task-%s_run-%s_bold_brain.nii.gz"%(sub, task, run))
            confounds=os.path.join(deriv_dir, sub, 'func','motion_assessment','%s_task-%s_run-%s_bold_brain_confound.txt'%(sub,task,run))
            
            main_dict[sub][run]['OUTPUT'] = output
            print("OUTPUT: ", output)
            print("FUNCTION: ", func)
            
            scan = func.split(".")[0]
            main_dict[sub][run]['FUNCRUN%i'%x] = scan
            ntmpts=check_output(['fslnvols', scan])
            ntmpts = ntmpts.decode('utf-8')
            ntmpts = ntmpts.strip('\n')
            main_dict[sub][run]['NTIMEPOINT%i'%x] = ntmpts
            print("TIMEPOINT: ", ntmpts)
                # -- CONFOUNDS

            main_dict[sub][run]['CONFOUND%i'%x] = confounds
            print("CONFOUNDS: ", confounds)

    # -- MOTION CORRECTION
            for i in range(6):
                motcor=os.path.join(data_dir, 'func','motion_assessment', 'motion_parameters','%s_task-%s_run-%s_moco%s.txt'%(sub,task,run,i))
                main_dict[sub][run]['MOCO%i'%i] = motcor
                print("MOTCOR: ", motcor)


    # -- TRS FROM NIFTI -- this value will always be 2, therefore we only run the check once
            trs=check_output(['fslval','%s'%(scan),'pixdim4',scan])
            trs=trs.decode('utf-8')
            trs=trs.strip('\n')
            print("TRs: ", trs)
            main_dict[sub][run]['TR'] = trs



    # -- EVS -- here we loop through the given EVs and add the corresponding file to the dictionary

            ctr=0
            for item in arglist['EV']:
            #print(item)
                ctr=ctr+1
                main_dict[sub][run]['EV%iTITLE'%ctr] = item
                ev=os.path.join(data_dir,'func','onsets','%s_task-%s_run-%s.txt'%(sub, item,run))


                #print("EV: ", ev)
                main_dict[sub][run]['EV%i'%ctr] = ev
            
            
            
def create_fsf():
    global main_dict
    main_dict= {}
    for sub_path in glob.glob(os.path.join(deriv_dir, 'sub-*')):
        sub=sub_path.split("/")[-1]
        set_dict(sub)
        fill_dict(sub)
        make_file(sub)

def main():
    set_parser()
    set_paths()
    create_fsf()
main()
