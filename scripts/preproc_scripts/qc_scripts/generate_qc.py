#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:58:40 2018

@author: nikkibytes

"""


from PyPDF2 import PdfFileMerger,PdfFileWriter, PdfFileReader
import os
import io
import cairosvg
import glob
from io import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



def makeHTML():
    os.chdir('/projects/niblab/bids_projects/Experiments/EricData/data/derivatives/pngs')
    pngs = glob.glob('*png')
    deriv_path = os.path.join(basepath, 'derivatives')
    outfile = os.path.join(deriv_path, "pngs", "CHOCO-DATA_ses-1_fmriprep_QC.html")
    f = open(outfile, "w")
    for file in pngs:
        sub = file.split("_")[0]
        task = file.split("_")[2]
        #if "training" in task:
        #    run = file.split("_")[3]
        #else:
        #    run = None
        print(sub, task )
        print("-------->", file)
        f.write("<p>SUBJECT: %s | SESSION 1 | %s "%(sub, task))
        f.write("<p>__________________________________________________________")
        f.write("<p>FILENAME: %s \n"%(file))
        f.write("<p><IMG SRC=\"%s\">"%(file))
    f.close()
def mergePDFs(sub):
    #pdfs = glob.glob(os.path.join(basepath, 'figures', '*.pdf'))
    pdfs = glob.glob(os.path.join(basepath, 'figures', '*.pdf'))
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)

    merger.write("result.pdf")

def getPDFs(dpath,sub, fpath):
    #data/fmriprep/ses-1/sub-001/fmriprep/sub-001
    #Experiments/EricData/data/fmriprep/sub-001/ses-1/fmriprep/sub-001/figures
    svgs= glob.glob(os.path.join(fpath, sub, 'ses-1',  'fmriprep', sub, 'figures', '*rois.svg'))
    for img in svgs:
        print('>>>>>SVG IMG: ', img)
        # get our current filename
        name = img.split('/')
        for word in name:
            if '.svg' in word:
                word = word.split('.')[0]
                filename=word+'.png'
        out=os.path.join(dpath, 'test', filename) #output pdf filename
        print(" %s ------> %s "%(img, out))
        cairosvg.svg2png(url=img, write_to=out) #convert svg
        if not os.path.exists(out):
            cairosvg.svg2pdf(url=img, write_to=out) #convert svg
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(10, 100, "W")
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(open(out, "rb"))
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        outputStream = open("Test_"+filename, "wb")
        output.write(outputStream)
        outputStream.close()
    #iterate through currently made images and write details to file


from reportlab.lib import utils

def get_image(path, width=1*cm):

for png in pngs:
     filename=png.split('.')[0]
     c = canvas.Canvas(filename+".pdf")
     c.setFont("Helvetica", 20)
     c.drawString(30, 750, "FILENAME: %s "%filename)
     c.drawImage(png, 0, 0, width=150, height=75)
     c.showPage()
     c.save()





def main():
    global basepath
    basepath= "/projects/niblab/bids_projects/Experiments/EricData/data"
    deriv_path = os.path.join(basepath, 'derivatives')
    fmriprep_path = os.path.join(basepath,'fmriprep')
    subs = glob.glob(os.path.join(deriv_path, 'sub-*'))
    print(" BASE DIRECTORY >>> %s \nFMRIPREP PATH >>> %s ")
    for sub_path in subs:
        words = sub_path.split('/')
        for w in words:
            if 'sub-' in w:
                sub = w
        print("FETCHING SVGS FIGURES FROM SUBJECT ... %s"%sub)
        getPDFs(deriv_path, sub, fmriprep_path)
        #mergePDFS(sub)
main()
