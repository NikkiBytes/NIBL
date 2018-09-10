import glob
import os

# Get base path, and check for existing QC file.
path="/projects/niblab/bids_projects/Experiments/bbx"
outfile=os.path.join(path, "BBx_ses-2_QC_fmriprep.html")
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
    f.write("<p><font size=12>fMRIprep Quality Check, BBx, Session 1</font><br>")
    f.write("<p><b><font size=10> %s </font></b><br>"%sub)
    print("---------------> WRITING ANATOMICAL FILES TO HTML ", sub)
    for file in sub_dict[subID]["T1w"]:
        if "brainmask" in file:
            t1_brainmask = file
        if "mni" in file:
            t1_mni = file
    f.write("<p><b><font size=8>Anatomical</font></b> <br> \
     Brain mask and brain tissue segmentation of the T1w <br> \
     <font size=4>FILENAME: %s </font><br><br><b><IMG SRC=\"%s\" WIDTH=1200> <br><br> \
     T1 to MNI registration <br> \
     <font size=4>FILENAME: %s </font><br><br><b><IMG SRC=\"%s\" WIDTH=1200> <br><br> \
     "%(t1_brainmask.split("/")[-1],t1_brainmask,t1_mni.split("/")[-1],t1_mni))
    print("---------------> WRITING FUNCTIONAL FILES TO HTML")
    f.write("<p><b><font size=8>Functional</font></b><br>")
    for file in sub_dict[sub]["REST"]:
        f.write("<p><b><font size=6>TASK-RESTING </font></b><br>")
        if "bold" in file:
            print(" >>>>>>>>>>>> WRITING BOLD RESTING FILES TO HTML ---------- FILE %s"%file)
            f.write("<p><font size=5> <b>ROIs in BOLD space </b> </font> <br> \
            <font size=4>FILENAME: %s </font> <br><br><IMG SRC=\"%s\" WIDTH=1200><br>"%(file.split("/")[-1],file))
        elif "carpetplot" in file:
            f.write("<p><font size=5> <b>BOLD Summary </b> </font> <br> \
            <font size=4>FILENAME: %s </font> <br><br><IMG SRC=\"%s\" WIDTH=1200><br>"%(file.split("/")[-1],file))
        else:
            print(" >>>>>>>>>>>> WRITING RESTING FILES TO HTML ---------- FILE %s"%file)
            f.write("<p><font size=5><b>EPI to T1 registration</b> </font> <br><font size=4> FILENAME: %s </font><br> <br> \
            <IMG SRC=\"%s\" WIDTH=1200> <br>"%file.split("/")[-1],file)
    for key2 in sub_dict[sub]:
        if "run" in key2:
            f.write("<p><b><font size=6>TASK-TRAINING </font></b><br>")
            print(" >>>>>>>>>>>> WRITING TRAINING FILES TO HTML")
            run = key2
            print("RUN >>>>>>>>>>>> %s"%run)
            roi = sub_dict[sub][run]["ROI"]
            epi2t1 = sub_dict[sub][run]["FLT"]
            carpet = sub_dict[subID][run]["CARPET"]
            f.write("<p><font size=5><b>%s</b></font><br><font size=5><b>ROIs in BOLD space </b></font> <br> \
            <font size=4>FILENAME: %s </font><br><br> <IMG SRC=\"%s\" WIDTH=1200><br> <b><font size=5> EPI to T1 registration </font> </b> <br> \
            <font size=4> FILENAME: %s </font><br> <br><IMG SRC=\"%s\" WIDTH=1200><br><br> <b><font size=5> BOLD Summary </font> </b> <br> \
            <font size=4> FILENAME: %s </font><br> <br><IMG SRC=\"%s\" WIDTH=1200><br>"%(run,roi.split("/")[-1],roi,epi2t1.split("/")[-1], epi2t1, carpet.split("/")[-1], carpet))


f.close()
