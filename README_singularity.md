### Running Singularity Containers
This README contains details for the currently available Singularity containers for fMRI data prep.

Log into RENCI:

        $ ssh -XY your_account@ht4.renci.org
        $ {your_password}


Access the Singularity Containers:

        $ cd /projects/niblab/bids_projects/Singularity_Containers


To run Singularity Containers:

*BIDS Validator* <br>
  Image: bids_validator.simg

      START THE INTERACTIVE SHELL:
              $ sinteractive
      START THE SINGULARITY IMAGE(FROM WITHIN __~/bids_projects__ directory)
              $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/bids_validator.simg

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
