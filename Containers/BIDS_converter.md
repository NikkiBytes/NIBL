## BIDS Converter with heudiconv

Image: heudiconv.simg

This container allows us to open up an environment to run the heudiconv converter and convert our data into BIDS format.

### Workflow: <br>
Log into RENCI --> Start Singularity shell --> Run commands


    heudiconv command:
          $ heudiconv -b -d {input_directory} -s {SUBJECT} -ss {SESSION} -f {heuristic_file} \
          -c dcm2niix -b  -o {output_directory}



  * Notes:\
    -- heuristic_file: Unique file of keys we must provide that tells how the files are to be converted. \
          We use the information from our dicominfo.txt to fill in our keys.


#### Examples

    Example: getting the dicominfo.tsv file

          $ heudiconv -d Data/{subject}/{session}/Dicoms/dicoms/*/*dcm -s Eric_Data \
          -ss wave2 -f convertall.py -c none -o /output/EricData/pre-bids_files

    Example: converting a single subject

          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/heudiconv.simg
          $ cd /test
          $ heudiconv -d Data/{subject}/{session}/Dicoms/dicoms/*/*dcm -s Eric_Data \
          -ss wave2 -f eric_conversion.py -c none -o output/EricData/ses-wave2

    Example: Converting all subjects
             To convert multiple subjects we can create a simple script that loops through our subjects.


          $ cd /projects/niblab/bids_projects
          $ sinteractive -m 24000
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/heudiconv.simg
          $ cd /test
          $ bash scripts/SugarMama_BIDS_conversion.sh

Refer to, <i>SugarMama_BIDS_conversion.sh</i>, for a template and further explanation of converting multiple subjects.
