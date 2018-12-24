# make onset directories and move ev files

import glob
import os
from shutil import copy


mlkDir = "/projects/niblab/data/eric_data/ev_files/milkshake"
mlkA = glob.glob(os.path.join(mlkDir, "mkA*"))
mlkB = glob.glob(os.path.join(mlkDir, "mkB*"))
mlkC = glob.glob(os.path.join(mlkDir, "mkC*"))
mlkD = glob.glob(os.path.join(mlkDir, "mkD*"))
subs = glob.glob(os.path.join("/projects/niblab/bids_projects/Experiments/EricData/data/derivatives", "sub-*"))

for sub in subs:
    funcDir = os.path.join(sub, "ses-4/func")
    newDest = os.path.join(sub, "ses-4/func/onsets")
    curr_mlks = glob.glob(os.path.join(funcDir, "*milkshake*"))
    if not curr_mlks:
        print(">>>>>>>>>>>>> NO DATA FOR ", sub.split("/")[-1])
        pass
    else:
        print(">>>>>>>>>>>>> SUBJECTS: ", sub.split("/")[-1])
        print(">>>>>>>>>>>>> MILKSHAKE FILES: ", curr_mlks)
        if not os.path.exists(newDest):
            os.makedirs(newDest)
        for milk in curr_mlks:
            filename = milk.split("/")[-1]
            filename = filename.split("_")
            for word in filename:
                if "milkshake" in word:
                    mlkID = word.split("e")[1]
                    print("MILKSHAKE ID >>>>>>>>>>>>>>>> ", mlkID)
            if mlkID == "A":
                for file in mlkA:
                    print("COPYING FILE %s >>>>>>>>>>>>>>>>>>>>>>>>>>>> %s" %(file, newDest))
                    copy(file, newDest)
            elif mlkID == "B":
                for file in mlkB:
                    print("COPYING FILE %s >>>>>>>>>>>>>>>>>>>>>>>>>>>> %s" %(file, newDest))
                    copy(file, newDest)
            elif mlkID == "C":
                for file in mlkC:
                    print("COPYING FILE %s >>>>>>>>>>>>>>>>>>>>>>>>>>>> %s" %(file, newDest))
                    copy(file, newDest)
            else:
                for file in mlkD:
                    print("COPYING FILE %s >>>>>>>>>>>>>>>>>>>>>>>>>>>> %s" %(file, newDest))
                    copy(file, newDest)
