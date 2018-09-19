"""
author: nicholletteacosta extended from original by Jeannette Mumford found @youtube -- Mumfordbrainstats

"""

import os
import glob

# We will start with the registration png files
outfile = "/projects/niblab/bids_projects/Experiments/BBx/derivatives/Level2_QA_BBx_ses-1.html"
os.system("rm %s"%(outfile))
subjects = glob.glob(os.path.join("/projects/niblab/bids_projects/Experiments/BBx/derivatives", "sub-*"))
f = open(outfile, "w")
f.write("<p><font size=8><b>STUDY: BBx</font></b><br><font size= 7>Session: 1</font><br><br><br>")
for sub_path in sorted(subjects):
    subID = sub_path.split("/")[-1]
    #ses-1/func/Analysis/feat2/sub-001.gfeat/inputreg
    IMGS_PATH = os.path.join(sub_path, "ses-1/func/Analysis/feat2", "%s.gfeat"%subID, "inputreg", "*.png")
    IMGS = glob.glob(IMGS_PATH)
    print(">>>>-------------> ID: %s"%subID)
    f.write("<p><font size=6>ID: <b>%s </b><br>"%subID)
    for img in sorted(IMGS):
        if "masksum" in img:
            print("WRITING IMAGE >>>>------------> %s "%img)
            f.write("<p><font size=5><b>SUM OF MASKS</b></font><br> \
            <IMG SRC=\"%s\" WIDTH=1200><br><br>"%img)
        else:
            print("WRITING IMAGE >>>>------------> %s "%img)
            f.write("<p><font size=5><b>UNIQUE MASKS</b></font><br> \
            <IMG SRC=\"%s\" WIDTH=1200><br><br>"%img)

f.close()
