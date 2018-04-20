## BIDS Validator

Workflow:
    I. Log into RENCI
    II. Start Singularity shell
    III. Validate BIDS dataset

    BIDS-validator command:
          $ bids-validator {data_directory}


Example:

    Testing Eric Data:
          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/bids_validator.simg
          $ cd /test
          $ bids-validator Experiments/EricData/EricData/ses-wave4
