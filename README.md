# Neuropsychology of Ingestive Behavior Lab (NIBL) @  UNC Chapel Hill

This repository contains the workflows for the various studies done in the lab.

## Directory of Experiment data:
          MAIN:           /projects/niblab/bids_projects/Experiments
          ERIC DATA:      /projects/niblab/bids_projects/Experiments/EricData/data
          BEVEL DATA:     /projects/niblab/bids_projects/Experiments/Bevel/data
          BBx:            /projects/niblab/bids_projects/Experiments/BBx/data


The **/Containers** folder contains the Singularity containers, workflows and scripts for running containers.

The **/Experiments** folder contains the labs, and their unique workflows.

The **/Osirix_Scrape** folder contains scripts used to data scrape all subjects from an experiment being stored on OsiriX Web Interface and transfer them to your HPC.

The **/BIDS_Conversion** folder contains relevant scripts for the BIDS conversion process. Here you will find an automated script for the conversion, '~/BIDSconversion.sh'. 
