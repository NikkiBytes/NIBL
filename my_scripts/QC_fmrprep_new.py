import glob
import os

# Get base path, and check for existing QC file.
path="/projects/niblab/bids_projects/Experiments/bbx"
outfile=os.path.join(path, "BBx_ses-1_QC_fmriprep.html")
os.remove(outfile)
f = open(outfile, 'w')

#get fmriprep path of all subjects --here we have set it to ses-2 (**may have to customize)
subjects = glob.glob(os.path.join(path, 'fmriprep', 'ses-1', 'sub-*'))
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
        svg_path = os.path.join(sub, 'fmriprep', 'sub-*', 'figures', '*svg')
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
                print(" >>>>>>>>>>>> WRITING TRAINING FILES TO HTML")
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
            REST_FLT_PATH =
        else:
            REST_CARPET_FILENAME = file.split("/")[-1]
            REST_CARPET_PATH = file

    for key2 in sub_dict[sub]:
        if "run" in key2:
            run = key2
            if "1" in run:
                ROIS_PATH_1 = sub_dict[sub][run]["ROI"]
                FLT_PATH_1 = sub_dict[sub][run]["FLT"]
                CARPET_PATH_1 = sub_dict[subID][run]["CARPET"]
            elif "2" in run:
                ROIS_PATH_2 = sub_dict[sub][run]["ROI"]
                FLT_PATH_2 = sub_dict[sub][run]["FLT"]
                CARPET_PATH_2 = sub_dict[subID][run]["CARPET"]
            elif "3" in run:
                BOLD_ROIS_PATH_3 = sub_dict[sub][run]["ROI"]
                FLT_PATH_3 = sub_dict[sub][run]["FLT"]
                CARPET_PATH_3 = sub_dict[subID][run]["CARPET"]
            else:
                ROIS_PATH_4 = sub_dict[sub][run]["ROI"]
                FLT_PATH_4 = sub_dict[sub][run]["FLT"]
                CARPET_PATH_4 = sub_dict[subID][run]["CARPET"]

    TITLE = """<p><font size=12>fMRIprep Quality Check, BBx, Session 1</font><br>
    <p><b><font size=10> "{SUB}" </font></b><br>"""
    ANATOMICAL = """<p><b><font size=8>Anatomical</font></b><br>
    <p><font size=6>Brain mask and brain tissue segmentation of the T1w </font><br>
    <font size=5>FILENAME: "{BRAINMASK_FILENAME}" </font><br><br>
    <IMG SRC=\"{BRAINMASK_PATH}\" WIDTH=1200> <br><br>
    <p><font size=6> T1 to MNI registration </font><br>
    <font size=5>FILENAME: "{MNI_FILENAME}" </font><br><br>
    <IMG SRC=\"{MNI_PATH}\" WIDTH=1200> <br><br>"""
    RESTING = """<p><b><font size=8>Functional</font></b><br>
    <font size=6>Task-Resting</font><br><br>
    <font size=6>ROIs in Bold Space</font><br>
    <font size=5>FILENAME: "{REST_ROI_FILENAME}"" </font> <br><br>
    <IMG SRC=\"{REST_ROI_FILE}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <font size=5>FILENAME: "{REST_FLT_FILENAME"" </font> <br><br>
    <IMG SRC=\"{REST_FLT_PATH}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <font size=5>FILENAME: "{REST_CARPET_FILENAME}"" </font> <br><br>
    <IMG SRC=\"{REST_CARPET_PATH}\" WIDTH=1200><br><br><br>"""
    RUN1 = """<p><b><font size=6>Task-training-run-1 </font></b><br>")
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{ROIS_PATH_1}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{FLT_PATH_1}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{CARPET_PATH_1}\" WIDTH=1200><br><br><br>"""
    RUN2 = """<p><b><font size=6>Task-training-run-2 </font></b><br>")
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{ROIS_PATH_2}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{FLT_PATH_2}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{CARPET_PATH_2}\" WIDTH=1200><br><br><br>"""
    RUN3 = """<p><b><font size=6>Task-training-run-3 </font></b><br>")
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{ROIS_PATH_3}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{FLT_PATH_3}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{CARPET_PATH_3}\" WIDTH=1200><br><br><br>"""
    RUN4 = """<p><b><font size=6>Task-training-run-4 </font></b><br>")
    <font size=6>ROIs in Bold Space</font><br>
    <IMG SRC=\"{ROIS_PATH_4}\" WIDTH=1200><br><br>
    <font size=6>EPI to T1 Registration</font><br>
    <IMG SRC=\"{FLT_PATH_4}\" WIDTH=1200><br><br>
    <font size=6>BOLD Summary</font><br>
    <IMG SRC=\"{CARPET_PATH_4}\" WIDTH=1200><br><br><br>"""
f.close()
