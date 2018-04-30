## BIDS Validator

Image: bids_validator.simg

### Workflow: <br>
Log into RENCI --> Start Singularity shell --> Validate BIDS dataset

    BIDS-validator command:
          $ bids-validator {data_directory}


Example:

    Validate Eric Data:
          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/bids_validator.simg
          $ cd /test
          $ bids-validator Experiments/EricData/EricData/ses-wave4
