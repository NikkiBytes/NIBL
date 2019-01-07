# Brain Imaging Data Structure (BIDS) Conversion  
  
Here we are going to describe the process of converting raw dicom files into the BIDS format for further analysis. For NIBL we utilize Singularity containers to run the processes on the high performance computing cluster(HPCC). Below you will find more details on the process and references to specific files found within this folder to use as a template. 


## Getting Started  

To get the data into BIDS format there is series of simples steps to follow to set up our data for conversion.  
```
I.      Rename Data folders
II.     Modify Heuristic File
III.    Setup batch script & run 
IV.     Modify post-BIDS data 
V.      Validate BIDS data
```


### What is Singularity?  
For our processes the Singularity container has already been built and we will use this to run our process. However understanding what it is may come in use if you ever need to modify or create your own container. Singularity containers can be used to pacakge scientific workflows, software and libraries and even data, and more importantly they support use on the HPCC. Creating a Singularity container may be beyond the scope of this topic, however we will provide documentation for those interested. Know that with the Singularity containeres we are able to package the `heudiconv` software and use it for our BIDS conversion. We are able to use the `exec` , `shell` , `run` and other commands, that allow us to run the software easily and with ease that feels similar to running software on a terminal. For our purposes we have utilized the `shell` and `exec` command, which will be discussed in further detail. 