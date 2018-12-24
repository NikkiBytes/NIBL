#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 14:58:40 2018

@author: nikkibytes
"""
import os 
import PyPDF2
import cairosvg
import glob
basepath= '/Users/nikkibytes/Documents/BevBits'
sub_imgs= glob.glob(os.path.join(basepath, 'figures', '*flt_bbr.svg'))
for img in sub_imgs:
    name = img.split('/')
    for word in name:  
        if '.svg' in word:
            word = word.split('.')[0]
            filename=word+'.pdf'
            print(filename)
            out=os.path.join(basepath,'figures','pdfs', filename)
            cairosvg.svg2pdf(url=img, write_to=out)
            