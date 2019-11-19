import glob
import os
import jinja2




def get_data(sub_id, study_path, ses_id, sub_dict):
    fmriprep_path = os.path.join(study_path, "bids/derivatives/fmriprep")
    # initialize dictionary
    sub_dict[sub_id] = {}

    # Get data:

    # anatomicals:
    t1w_brainmask_svg = os.path.join(fmriprep_path, sub_id, 'figures', '{}_space-MNI152NLin2009cAsym_T1w.svg'.format(sub_id))
    sub_dict[sub_id]["ANAT"]  = t1w_brainmask_svg

    # fieldmaps:
    fmap_svg = os.path.join(fmriprep_path, sub_id, 'ses-'+ses_id, 'figures', '{}_ses-{}_desc-brain_mask.svg'.format(sub_id, ses_id))
    sub_dict[sub_id]["FMAP"] = fmap_svg

    # functionals
    func_fmaps=glob.glob(os.path.join(fmriprep_path, sub_id, 'ses-'+ses_id, 'figures', '{}_ses-{}_*desc-fieldmap_bold.svg'.format(sub_id, ses_id) ))
    func_sdcs=glob.glob(os.path.join(fmriprep_path, 'sub-*', 'ses-'+ses_id, 'figures', '{}_ses-{}_*desc-sdc_bold.svg'.format(sub_id, ses_id)))
    func_flirts=glob.glob(os.path.join(fmriprep_path, 'sub-*', 'ses-'+ses_id, 'figures','{}_ses-{}_*_desc-flirtbbr_bold.svg'.format(sub_id, ses_id)))
    sub_dict[sub_id]["FUNC_FMAPS"] = func_fmaps
    sub_dict[sub_id]["FUNC_SDCS"] = func_sdcs
    sub_dict[sub_id]["FUNC_FLIRTS"] = func_flirts

def make_html(sub_dict):
    env = jinja2.Environment(loader=jinja2.PackageLoader('app'))
    template = env.get_template('base.html')

    filename = os.path.join("html/base.html")

    with open(filename, "w") as fh:
        fh.write(template.render(
            Title = "BBx Session 1 fmriprep QC",
            data_dict = sub_dict

        ))




def main():
    # Get base path, and check for existing QC file.
    #study_path = "/projects/niblab/bids_projects/Experiments/bbx"
    study_path = "/qc_generator/data/bbx"
    # outfile=os.path.join(path, "bids/derivatives/bbx_ses-1_QA_fmriprep.html")
    # os.remove(outfile)
    # f = open(outfile, 'w')
    sess_id = "ses-1"
    # get fmriprep path of all subjects --here we have set it to ses-2 (**may have to customize)
    sub_ids = [x.split("/")[-1] for x in glob.glob(os.path.join(study_path, 'bids/derivatives/fmriprep', 'sub-*'))]
    sub_dict = {}
    #print(sub_ids)
    for sub_id in sub_ids:
        get_data(sub_id, study_path, "1", sub_dict)
    #print(sub_dict)
    for i in sub_dict:
        print(sub_dict[i]["FMAP"])
    make_html(sub_dict)
if __name__ == "__main__":
    main()