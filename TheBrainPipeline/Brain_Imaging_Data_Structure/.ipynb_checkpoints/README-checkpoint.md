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
For our processes the Singularity container has already been built and we will use this to run our conversion. Creating a Singularity container may be beyond the scope of this topic, however we will provide documentation for those interested, understanding what it is may come in use if you ever need to modify or create your own container. Singularity containers can be used to pacakge scientific workflows, software and libraries and even data, and more importantly they support use on the HPCC. The key here is to know that with the Singularity container we are able to package the `heudiconv` software and use it for our BIDS conversion. We are able to use the container commands that allow us to run the software easily and with ease that feels similar to running software on a terminal. For our purposes we have utilized the `shell` and `exec` command, which will be discussed in further detail.   
  
  
## BIDS Conversion Workflow 
*this workflow assumes you already have your data on RENCI   
  
  
### Rename Directories  
One of the specifications of BIDS is the naming scheme. While this can be meticulous it allows for a standardized format that can be understood. To avoid complex programming down the line I found it was easiest to name our directories into the BIDS format before our conversion. BIDS expects to find, `sub-XXX`, where `XXX` can be any identifier. In many cases this is straight forward, however every dataset is different and there can be nuances that make it difficult to make an all encompassing script for renaming. However the script [Rename_Folders.ipynb](ADD_LINK_HERE) is flexible enough and should be able to guide you through renaming your directories!  
  
  
### Setting up the Heuristic File  
A great explanation is found here: [Using Heudiconv](http://nipy.org/heudiconv/#21)  
Then you can modify the template we have here: [Heuristic File template](ADD_LINK_HERE)  

  
### Setup batch script & run 
Here we are going to go over the batch script and setting it up.  
Reference the batch script here for reference: [Batch script](ADD_LINK_HERE)