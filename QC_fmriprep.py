from bs4 import BeautifulSoup
import glob
import os
from fpdf import FPDF

fpath = "/projects/niblab/bids_projects/Experiments/BBx/fmriprep/ses-1/sub-*/fmriprep/sub*.html"
htmls = glob.glob(fpath)


svgpath = "/projects/niblab/bids_projects/Experiments/BBx/fmriprep/ses-1/sub-*/fmriprep/sub-*/figures/*rois.svg"
pngpath = "/projects/niblab/bids_projects/Experiments/BBx/derivatives/pngs"
os.chdir(pngpath)
pngs= glob.glob("*.png")

png_dict = { }
for image in pngs:
    print("IMAGE: ", image)
    sub = image.split("_")[0]
    #print(sub, task, run)
    if sub not in png_dict:
        print("----------> MAKING DICTIONARY")
        png_dict[sub] = []
        png_dict[sub].append(image)
        #png_dict[sub]["PNGS"] = image
    else:
        png_dict[sub].append(image)
        print("#######%s DICTIONARY SUB: %s###########" %(sub, png_dict[sub]))



outpath =  "/projects/niblab/bids_projects/Experiments/BBx/derivatives/pdfs"
os.chdir(outpath)
pdf = FPDF()
titlepage = "BBx Quality Check \nPart 1: fMRIprep preprocessing \nSession 1"
pdf.set_title("BBx Session 1 QC Part A")
pdf.add_page()
pdf.set_font('Arial', 'B', 15)
pdf.multi_cell(0,20, titlepage, 0, 0, 'C' )
for sub in png_dict:
    print("UNSORTED DICTIONARY -----------> %s"%png_dict[sub])
    png_dict[sub] = sorted(png_dict[sub])
    print("SORTED DICTIONARY -----------> %s"%png_dict[sub])
    for image in png_dict[sub]:
            fullimg = pngpath+"/"+image
            print("-------------------------> WRITING TO PDF")
            print("FULL IMAGE PATH ------> %s"%(fullimg))
            task = image.split("_")[2]
            taskid = task.split('-')[1]
            id = sub.split('-')[1]
            print("----> IS RESTING? ")
            if 'resting' not in task:
                print("-------------> NOT")
                run = image.split("_")[3]
                runid = run.split('-')[1]
            else:
                print("--------------> TRUE")
                run = None
                runid = None
            lineA = "SUBJECT: %s || TASK: %s || RUN:  %s || \nFILENAME: %s "%(id, taskid, runid, image)
            print("LINE A : %s "%(lineA))
            pdf.add_page()
            pdf.image(fullimg, 5,50, 200)
            pdf.set_font('Arial', 'B', 15)
            pdf.multi_cell(0, 20, lineA, 0, 0)
pdf.output("yourfile.pdf", "F")
