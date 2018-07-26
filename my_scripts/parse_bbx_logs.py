
# coding: utf-8

# In[1]:


import numpy
import os
import pdb
import glob
import pandas as pd


# In[2]:


logpath = "/Users/nikkibytes/Documents/bbx_logs_all/logs"


# In[3]:


os.chdir(logpath)


# In[75]:


for file in glob.glob("bbx*.log"):
   # print(file)
    sub= "sub-"+file.split("_")[1]
    session = "ses-"+file.split("_")[3]
    run = "run-"+file.split("_")[2].split("n")[1]

    #print(sub, session, run)
    try:
        df = pd.read_csv(file, engine="python", sep="\\t", header=None)
        df.columns = ["onset", "data", "keypress"]
        df = df[["onset", "data"]]
    except pd.errors.EmptyDataError:
        print("EMPTY FILE ", file)

    start = df[df["data"].str.contains("start key press")]
    tasty = df[df["data"].str.contains("image=SL.jpg|image=CO.jpg")]
    ntasty = df[df["data"].str.contains("image=USL.jpg|image=UCO.jpg")]
    water = df[df["data"].str.contains("image=water.jpg")]
    NN = df[df["data"].str.contains("Level injecting via pump at address 0")]
    TT = df[df["data"].str.contains("Level injecting via pump at address 1")]
    UU = df[df["data"].str.contains("Level injecting via pump at address 2")]
    rinse = df[df["data"].str.contains("Level RINSE")]

    start = start[["onset"]]
    start_time = float(start.iat[0,0])

    tasty = tasty[["onset"]]
    ntasty = ntasty[["onset"]]
    water = water[["onset"]]
    NN = NN[["onset"]]
    TT = TT[["onset"]]
    UU = UU[["onset"]]
    rinse = rinse[["onset"]]


    tasty = tasty["onset"] - start_time
    ntasty = ntasty["onset"] - start_time
    water = water["onset"] - start_time
    NN = NN["onset"] - start_time

    TT = TT["onset"] - start_time

    UU = UU["onset"] - start_time

    rinse = rinse["onset"] - start_time


    outpath = "/Users/nikkibytes/Documents/bbx_logs_all/output/"

    files2make=['rinse', 'TT', 'UU', 'NN', 'Tcue', 'Ucue', 'Ncue']

    for name in files2make:
        filename = "%s_%s_%s_%s.txt"%(sub, session, name, run)
        if name == "rinse":
            rinse.to_csv(outpath+filename, header=None, index=None)
        elif name == "TT":
            TT.to_csv(outpath+filename, header=None, index=None)
        elif name == "UU":
            UU.to_csv(outpath+filename, header=None, index=None)
        elif name == "NN":
            NN.to_csv(outpath+filename, header=None, index=None)
        elif name == "Tcue":
            tasty.to_csv(outpath+filename, header=None, index=None)
        elif name == "Ucue":
            ntasty.to_csv(outpath+filename, header=None, index=None)
        else:
            water.to_csv(outpath+filename, header=None, index=None)


#print(tasty.head())
#tasty.to_csv(outpath+"/test_text.txt",header=None, index=None)
