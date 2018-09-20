import glob
import os
DER_DIR = "/projects/niblab/bids_projects/Experiments/Bevel/data/derivatives"
SUB_DIR = "/projects/niblab/bids_projects/Experiments/Bevel/data/derivatives/sub-*"
SUB_DIRS = glob.glob(SUB_DIR)

for sub in SUB_DIRS:
    subject = sub.split("/")[-1]
    #check for existence of feat2 directory
    FEAT2_DIR = os.path.join(sub, "func/Analysis/feat2")
    if os.path.exists(FEAT2_DIR):
        pass
    else:
        os.makedirs(FEAT2_DIR)
    print("> STARTING PROGRAM......")
    print("----------------------->>>>SUBJECT: ",sub)
    FEATS_PATH = os.path.join(sub, "func/Analysis/feat1/*.feat")
    FEATS = glob.glob(FEATS_PATH)
    with open(os.path.join(DER_DIR, "feat2_design_bevel.fsf"), 'r') as infile:
        tempfsf=infile.read()
        # set outpath for fsf OUTPATH variable, by run
        outpath = os.path.join(sub, "func/Analysis/feat2")
        print(">>>>>>>>>>>>>>>>>SETTING DESIGN OUTPATH: ", outpath)
        tempfsf = tempfsf.replace("OUTPUT", outpath)
        print(FEATS)
        for run_path in FEATS:
            run = run_path.split("/")[-1].split(".")[0]
            print(">>>>>------> RUN: ", run)
            if run == "run1":
                print("> %s : %s"%(run, run_path))
                tempfsf = tempfsf.replace(run, run_path)
            elif run == "run2":
                print("> %s : %s"%(run, run_path))
                tempfsf = tempfsf.replace(run, run_path)
            elif run == "run3":
                print("> %s : %s"%(run, run_path))
                tempfsf = tempfsf.replace(run, run_path)
            else:
                print("> %s : %s"%(run, run_path))
                tempfsf = tempfsf.replace(run, run_path)
        OUTFILE_PATH = os.path.join(FEAT2_DIR, "%s_design.fsf"%subject)
        print("OUTFILE ------------------------>>>> ", OUTFILE_PATH)
        with open(OUTFILE_PATH, "w") as outfile:
            outfile.write(tempfsf)
        outfile.close()
    infile.close()
