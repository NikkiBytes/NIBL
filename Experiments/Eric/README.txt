



To view Eric Data:
    $ cd /projects/niblab/bids_projects/Experiments/EricData
    $ ls


To run Singularity Containers:

-->fmriprep_container.simg

      I. Log into RENCI
      II. Run commands to change to the directory and run the fmriprep singularity Containers

          $ cd /projects/niblab/bids_projects/Singularity_Containers
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/mydirectory /projects/niblab/bids_projects/Singularity_Containers/fmriprep_container.simg
          $ cd /mydirectory/Experiments/EricData
          $ fmriprep /mydirectory/Experiments/EricData/EricData/ses-wave4 fmriprep_run \
              participant  \
              --participant-label 001 002 \
              --fs-license-file /mydirectory/freesurfer/license.txt \
              --ignore slicetiming --t2s-coreg --output-space T1w --template {MNI152NLin2009cAsym} \
              --debug






************************************************

Eric Data BIDS Directory

/EricData
  /sub-001
    /ses-wave1
      /fmap
          /sub-01_phasediff
          /sub-01_magnitude
      /func
          --> ep2d_pace_moco_milkshake_A
          --> ep2d_pace_moco_milkshake_B
          --> ep2d_pace_moco_milkshake_C
          --> ep2d_pace_moco_milkshake_D
          --> ep2d_pace_moco_Go_NoGo2
          --> ep2d_pace_moco_Go_NoGo1
          --> ep2d_pace_moco_imagine

      /anat
          --> t1_mprage_tra_NEW!!
            /sub-01_T1w.nii.gz
            /sub-01_T1w.json
    /ses-wave2
    /ses-wave3
    /ses-wave4

*************************************************


WAVE4 Misc. Info

  Logs - 111
  Dicoms - 99

  Subject IDS:

  001  008  018  033  043  049  056  062  071  079  088  094  101  107  116  122  131
  002  011  022  034  044  051  057  063  072  081  089  095  102  109  117  123  132
  004  012  028  037  045  052  058  064  075  082  090  096  103  110  118  126  154
  005  013  029  040  046  053  059  065  076  083  091  097  104  113  119  127
  006  014  030  041  047  054  060  066  077  084  092  098  105  114  120  128
  007  017  032  042  048  055  061  068  078  085  093  099  106  115  121  130
