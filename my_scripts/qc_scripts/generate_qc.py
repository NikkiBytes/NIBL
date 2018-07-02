#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:58:40 2018

@author: nikkibytes

"""


from PyPDF2 import PdfFileMerger
import os 
import cairosvg
import glob
basepath= '/Users/nikkibytes/Documents/BevBits'
svgs= glob.glob(os.path.join(basepath, 'figures', '*flt_bbr.svg'))

for img in svgs:
    name = img.split('/')
    for word in name:  
        if '.svg' in word:
            word = word.split('.')[0]
            filename=word+'.pdf'
            
            out=os.path.join(basepath,'figures', filename)
            cairosvg.svg2pdf(url=img, write_to=out)

pdfs = glob.glob(os.path.join(basepath, 'figures', '*.pdf'))

merger = PdfFileMerger()


for pdf in pdfs: 
    merger.append(pdf)

merger.write("result.pdf")