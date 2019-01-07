# Brain Imaging Data Structure (BIDS) Conversion  
  
Here we are going to describe the process of converting raw dicom files into the BIDS format for further analysis. For NIBL we utilize Singularity containers to run the processes on the high performance computing cluster(HPC). Below you will find more details on the process and references to specific files found within this folder to use as a template. 


## Getting Started  

To get the data into BIDS format there is series of simples steps to follow to set up our data for conversion.  
```
I.      Rename Data
II.     Modify Heuristic File
III.    Setup batch script & run 
IV.     Modify post-BIDS data 
V.      Validate BIDS data
```


