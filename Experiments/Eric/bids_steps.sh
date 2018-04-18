singularity shell -B /projects/niblab/bids_projects:/test heudiconv.simg


heudiconv -d Data/{subject}/{session}/dicoms/*/*dcm -s Eric_Data -ss wave1 -f ConversionFiles/convertall.py -c none -o Experiments/EricData/bids_prep
