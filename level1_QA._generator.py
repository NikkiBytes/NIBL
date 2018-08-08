"""
author: nicholletteacosta extended from original by Jeannette Mumford found @youtube -- Mumfordbrainstats

"""

import os
import glob

# We will start with the registration png files
outfile = "/projects/niblab/bids_projects/Experiments/BBx/derivatives/Level1_QA_BBx_ses-1.html"
os.system("rm %s"%(outfile))
all_feats = glob.glob(os.path.join("/projects/niblab/bids_projects/Experiments/BBx/derivatives", "sub-*", "ses-1", "func", "Analysis", "feat1", "run*.feat"))
f = open(outfile, "w")

for file in list(all_feats):
  f.write("<p>============================================")
  f.write("<p>%s"%(file))
  f.write("<IMG SRC=\"%s/design.png\">"%(file))
  f.write("\n")
  f.write("<IMG SRC=\"%s/design_cov.png\" >"%(file))
  f.write("<p><IMG SRC=\"%s/reg/example_func2standard1.png\" WIDTH=1200>"%(file))
  f.write("<p><IMG SRC=\"%s/reg/example_func2standard.png\" WIDTH=1200>"%(file))
f.close()
