Information for Eric Data BIDS Conversion and fmriprep 

To view Eric Data:
    $ cd /projects/niblab/bids_projects/Experiments/EricData 
    $ ls

To run Singularity Containers:


BIDS Validator
  Image --> ~/Singularity_Containers/bids_validator.simg

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
      II. Run the /run_fmriprep.sh file:
              /projects/niblab/bids_projects
              
          Or run the fmriprep singularity Containers

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






************************************************

Eric Data BIDS Directory
Currently ~

[ *Note 
    -- for task files, under ~/func there are 2 files for each task,
                the original file, e.g. 'sub-001_task-milkshake_A.json',
                and the motion corrected file identified with [_physio], e.g. 'sub-001_task-milkshake_A_physio.json' ]
                
               
/EricData
  /ses-wave4
    /sub-001
      /fmap
          /sub-001_phasediff.json{nii.gz}
          /sub-001_magnitude1.json{nii.gz}
          /sub-001_magnitude2.json{nii.gz}
      /func
          /sub-001_task-milkshake_A[_physio].json{nii.gz}
          /sub-001_task-milkshake_B[_physio].json{nii.gz}
          /sub-001_task-milkshake_C[_physio].json{nii.gz}
          /sub-001_task-milkshake_D[_physio].json{nii.gz}
          /sub-001_task-imagine[_physio].json{nii.gz}
          /sub-001_task-Go_NoGo2[_physio].json{nii.gz}
          /sub-001_task-Go_NoGo1[_physio].json{nii.gz}
      /anat
          /sub-01_T1w.json{nii.gz}
       


*************************************************


WAVE4 Misc. Info

  Logs - 111
  Dicoms - 98
  Available Tasks - GoNo1, GoNo2, imagine, milkshakeA, milkshakeB, milkshakeC, milkshakeD 
  
  Subject IDS:

  001  008  018  033  043  049  056  062  071  079  088  094  101  107  116  122  131
  002  011  022  034  044  051  057  063  072  081  089  095  102  109  117  123  132
  004  012  028  037  045  052  058  064  075  082  090  096  103  110  118  126  154
  005  013  029  040  046  053  059  065  076  083  091  097  104  113  119  127
  006  014  030  041  047  054  060  066  077  084  092  098  105  114  120  128
  007  017  032  042  048  055  061  068  078  085  093  099  106  115  121  130
