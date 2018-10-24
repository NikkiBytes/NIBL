from nilearn import image 
import glob, os

# get data
sessions = ["ses-2", "ses-3", "ses-4"]
data_path = "/projects/niblab/bids_projects/Experiments/ChocoData/derivatives"
SUBS = sorted(glob.glob(os.path.join(data_path, "sub-*")))
for sub_path in SUBS:
    for ses in sessions:
        ses_path = os.path.join(sub_path, ses)
        if not os.path.exists(ses_path):
            pass
        else:
            ## path exists == session exists, continue with conversion
            ## get functional images 
            FUNCS = glob.glob(os.path.join(ses_path, "func", "*bold_brain.nii.gz"))
            for epi_file in FUNCS:
                filename = epi_file.split("/")[-1]
                subID = filename.split("_")[0]
                task = filename.split("_")[2]
                new_filename = os.path.join(ses_path, "func/%s_%s_%s_smoothed.nii.gz"%(subID, ses, task))
                mean_func = image.mean_img(epi_file)
                smoothed_img = image.smooth_img(mean_func, fwhm=5)
                smoothed_img.to_filename(new_filename)
                
