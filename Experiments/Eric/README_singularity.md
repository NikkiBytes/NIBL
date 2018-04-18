### Eric Data Preprocessing Steps and Singularity Containers
Below are detailed steps to pre-processing Eric Data with the containers.


To run Singularity Containers:

BIDS Validator
  Image --> ~Singularity_Containers/bids_validator.simg

    I. Log into RENCI

    II. Open Image
      $ cd /projects/niblab/bids_projects
      $ sinteractive
      $ singularity shell -B /projects/niblab/bids_projects:/test \
        Singularity_Containers/bids_validator.simg
    III. Go to Data You want verified
        -- for Eric Data we will eventually test all entire study with all
        -- waves, for now we are testing one session, follow below:
      $ cd /test/Experiments/EricData/EricData
    IV. Run bids-validator to test
      $ bids-validator ses-wave4




fMRI Prep
  Image --> ~/Singularity_Containers/fmriprep_container.simg

      I. Log into RENCI
      II. Workflow to run fmriprep on one subject:

          $ cd /projects/niblab/bids_projects/Singularity_Containers
          $ sinteractive -m 24000
          $ singularity shell -B /projects/niblab/bids_projects:/mydirectory \
           /projects/niblab/bids_projects/Singularity_Containers/fmriprep_container.simg
          $ cd /mydirectory
          $ fmriprep Experiments/EricData/EricData/ses-wave4 fmriprep_run \
              participant  \
              --participant-label 001 -t milkshakeA \
              --fs-license-file freesurfer/license.txt \
              --nthreads 8 --omp-nthreads 16 --low-mem \
              --ignore slicetiming \
              --output-space T1w --template MNI152NLin2009cAsym \
              --fs-no-reconall --debug --anat-only \
              -w intermediate_results --resource-monitor --write-graph --stop-on-first-crash
