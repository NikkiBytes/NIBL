
sinteractive -m 24000
singularity shell -B /projects/niblab/bids_projects:/mydirectory \
 /projects/niblab/bids_projects/Singularity_Containers/fmriprep_container.simg

cd /projects/niblab/bids_proj

singularity shell -B /projects/niblab/bids_projects:/mydirectory \
/projects/niblab/bids_projects/Singularity_Containers/fmriprep_container.simg
cd /mydirectory
fmriprep Experiments/EricData/EricData/ses-wave4 fmriprep_run \
    participant  \
    --participant-label 001  \
    --fs-license-file freesurfer/license.txt \
    --nthreads 8 --omp-nthreads 16 --low-mem \
    --ignore slicetiming  \
    --output-space T1w --template MNI152NLin2009cAsym \
    --fs-no-reconall --debug --anat-only \
    -w intermediate_results --resource-monitor --write-graph --stop-on-first-crash
