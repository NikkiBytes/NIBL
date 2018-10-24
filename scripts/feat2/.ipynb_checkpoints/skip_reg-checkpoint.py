# Skipping REGISTRATION

# Check for reg_standard folder --delete if exists
import glob
import os
import shutil
subjects=glob.glob("/projects/niblab/bids_projects/Experiments/bbx/derivatives/sub-*")
for sub in subjects:
    REGSTD_DIR = os.path.join(sub, "ses-1/func/Analysis/feat1/*run*+.feat/reg_standard")
    regstandard_dirs = glob.glob(REGSTD_DIR)
    if not regstandard_dirs:
        pass
    else:
        for dir in regstandard_dirs:
            print("--------------------------------------->>>> REMOVING REG_STANDARD DIRECTORY")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", dir)
            shutil.rmtree(dir)
    mat_path = os.path.join(sub, "ses-1/func/Analysis/feat1/*run*.feat/reg/*.mat")
    MAT_DIRS = glob.glob(mat_path)
    for file in MAT_DIRS:
        print("--------------------------------------->>>> REMOVING MAT FILES")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", file)
        os.remove(file)
    REG_PATH = os.path.join(sub, "ses-1/func/Analysis/feat1/*run*.feat/reg")
    REG_PATHS=glob.glob(REG_PATH)
    for file in REG_PATHS:
        path="%s/example_func2standard.mat"%file
        copy_mat_cmd="cp $FSLDIR/etc/flirtsch/ident.mat %s"%path
        print("--------------------------------------->>>> COPYING IDENTITY MATRIX")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", copy_mat_cmd)
        os.system(copy_mat_cmd)
    FEAT_PATH = os.path.join(sub, "ses-1/func/Analysis/feat1/*run*.feat")
    FEAT_PATHS = glob.glob(FEAT_PATH)
    for file in FEAT_PATHS:
        MEAN_PATH = os.path.join(file, "mean_func.nii.gz")
        REG_DIR = os.path.join(file, "reg", "standard.nii.gz")
        print("------------------>>>> ", MEAN_PATH)
        print("------------------>>>> ", REG_DIR)
        copy_mean_cmd = "cp %s %s"%(MEAN_PATH, REG_DIR)
        print("--------------------------------------->>>> COPYING MEAN FILE")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", copy_mean_cmd)
        os.system(copy_mean_cmd)
