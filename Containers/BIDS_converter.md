## BIDS Converter with heudiconv

Image: heudiconv.simg

This container allows us to open up an environment to run the heudiconv converter and convert our data into BIDS format.

### Workflow: <br>
Log into RENCI --> Start Singularity shell --> Run commands


    heudiconv command:
          $ heudiconv -b -d {input_directory} -s {SUBJECT} -ss {SESSION} -f {conversion_file} -c dcm2niix -b  -o {output_directory}




Example:

    Testing Eric Data:
          $ cd /projects/niblab/bids_projects
          $ sinteractive -m 24000
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/heudiconv.simg
          $ cd /test/Data/Eric_Data/wave1/dicoms
          $ subjects=(*)
          $ cd /test

          $ bids-validator Experiments/EricData/EricData/ses-wave4
