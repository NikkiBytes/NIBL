import glob
import os

# Get base path, and check for existing QC file.
path="/projects/niblab/bids_projects/Experiments/bbx"
outfile=os.path.join(path, "bbx_ses-1_QA_fmriprep.html")
os.remove(outfile)
f = open(outfile, 'w')
sess_id = "ses-1"
#get fmriprep path of all subjects --here we have set it to ses-2 (**may have to customize)
subjects = glob.glob(os.path.join(path, 'fmriprep', 'sub-*'))
sub_dict = {}

def make_dict(ID):
    sub_dict[ID] = {
            "REST" : [],
            "T1w" : [],
            }


def make_run(sID, rID):
    sub_dict[sID][rID] = {
            "ROI" : None,
            "FLT" : None,
            "CARPET" : None
            }

for sub in subjects:
        subID = sub.split("/")[-1]
        print("SUBJECT ---------------------------> ", subID)
        make_dict(subID)
        #f.write("\nSUBJECT ID: %s \n"%subID)
        svg_path = os.path.join(sub, sess_id, 'fmriprep', 'sub-*', 'figures', '*svg')
        svgs = glob.glob(svg_path)
        for svg in svgs:
            #print(svg)
            if "T1w" in svg:
                print(">>>>>>>>>WRITING T1w to DICT")
                sub_dict[subID]["T1w"].append(svg)
            elif "resting" in svg:
                print(">>>>>>>>>WRITING RESTING to DICT")
                sub_dict[subID]["REST"].append(svg)
            else:
                runID = svg.split("/")[-1].split("_")[3]
                if runID not in sub_dict[subID]:
                    make_run(subID,runID)
                if "rois" in svg:
                    sub_dict[subID][runID]["ROI"] = svg
                elif "flt_bbr" in svg:
                    sub_dict[subID][runID]["FLT"] = svg
                else:
                    sub_dict[subID][runID]["CARPET"] = svg
                print("RUN ID : ", runID)

for sub in sorted(sub_dict):
    for file in sub_dict[subID]["T1w"]:
        if "brainmask" in file:
            BRAINMASK_PATH = file
        if "mni" in file:
            MNI_PATH = file
    BRAINMASK_FILENAME = BRAINMASK_PATH.split("/")[-1]
    MNI_FILENAME = MNI_PATH.split("/")[-1]
    for file in sub_dict[sub]["REST"]:
        if "bold_rois" in file:
            REST_ROI_FILENAME = file.split("/")[-1]
            REST_ROI_FILE = file
        elif "bold_flt_bbr" in file:
            REST_FLT_FILENAME = file.split("/")[-1]
            REST_FLT_PATH =file
        else:
            REST_CARPET_FILENAME = file.split("/")[-1]
            REST_CARPET_PATH = file
    for key2 in sub_dict[sub]:
        if "run" in key2:
            run = key2
            if "1" in run:
                ROIS_PATH_1 = sub_dict[sub][run]["ROI"]
                FLT_PATH_1 = sub_dict[sub][run]["FLT"]
                CARPET_PATH_1 = sub_dict[sub][run]["CARPET"]
            elif "2" in run:
                ROIS_PATH_2 = sub_dict[sub][run]["ROI"]
                FLT_PATH_2 = sub_dict[sub][run]["FLT"]
                CARPET_PATH_2 = sub_dict[sub][run]["CARPET"]
            elif "3" in run:
                ROIS_PATH_3 = sub_dict[sub][run]["ROI"]
                FLT_PATH_3 = sub_dict[sub][run]["FLT"]
                CARPET_PATH_3 = sub_dict[sub][run]["CARPET"]
            else:
                ROIS_PATH_4 = sub_dict[sub][run]["ROI"]
                FLT_PATH_4 = sub_dict[sub][run]["FLT"]
                CARPET_PATH_4 = sub_dict[sub][run]["CARPET"]
    TITLE = """<p><font size=12>fMRIprep Quality Check, BBx, Session 1</font><br>
    <p><font size=7>ID: {SUB} </font><br>"""
    CURR_TITLE = TITLE.format(SUB=sub)
    f.write(CURR_TITLE)
    ANATOMICAL = """<p><b><u><font size=6>Anatomical</font></u></b><br>
    <p><font size=6>Brain mask and brain tissue segmentation of the T1w </font><br>
    <IMG SRC=\"{BRAINMASK_PATH}\" WIDTH=1200> <br><br>
    <p><font size=6> T1 to MNI registration </font><br>
    <IMG SRC=\"{MNI_PATH}\" WIDTH=1200> <br><br>"""
    CURR_ANAT = ANATOMICAL.format(BRAINMASK_PATH=BRAINMASK_PATH, MNI_PATH=MNI_PATH)
    f.write(CURR_ANAT)
    RESTING = """<p><b><u><font size=6>Functional</u></font></b><br>
    <font size=6>Task-Resting</font><br><br>
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{REST_ROI_FILE}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{REST_FLT_PATH}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{REST_CARPET_PATH}\" WIDTH=1200><br><br><br>"""
    CURR_REST = RESTING.format(REST_ROI_FILE=REST_ROI_FILE, REST_FLT_PATH=REST_FLT_PATH, REST_CARPET_PATH=REST_CARPET_PATH)
    f.write(CURR_REST)
    RUN1 = """<p><b><font size=6>Task-training-run-1 </font></b><br>")
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{ROIS_PATH_1}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{FLT_PATH_1}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{CARPET_PATH_1}\" WIDTH=1200><br><br><br>"""
    CURR_RUN1 =RUN1.format(ROIS_PATH_1=ROIS_PATH_1, FLT_PATH_1=FLT_PATH_1, CARPET_PATH_1=CARPET_PATH_1)
    f.write(CURR_RUN1)
    RUN2 = """<p><b><font size=6>Task-training-run-2 </font></b><br>")
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{ROIS_PATH_2}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{FLT_PATH_2}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{CARPET_PATH_2}\" WIDTH=1200><br><br><br>"""
    CURR_RUN2 = RUN2.format(ROIS_PATH_2=ROIS_PATH_2, FLT_PATH_2=FLT_PATH_2, CARPET_PATH_2=CARPET_PATH_2)
    f.write(CURR_RUN2)
    RUN3 = """<p><b><font size=6>Task-training-run-3 </font></b><br>")
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{ROIS_PATH_3}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{FLT_PATH_3}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{CARPET_PATH_3}\" WIDTH=1200><br><br><br>"""
    CURR_RUN3 = RUN3.format(ROIS_PATH_3=ROIS_PATH_3, FLT_PATH_3=FLT_PATH_3, CARPET_PATH_3=CARPET_PATH_3)
    f.write(CURR_RUN3)
    RUN4 = """<p><b><font size=6>Task-training-run-4 </font></b><br>")
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{ROIS_PATH_4}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{FLT_PATH_4}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{CARPET_PATH_4}\" WIDTH=1200><br><br><br>"""
    CURR_RUN4 = RUN4.format(ROIS_PATH_4=ROIS_PATH_4, FLT_PATH_4=FLT_PATH_4, CARPET_PATH_4=CARPET_PATH_4)
    f.write(CURR_RUN4)
f.close()
