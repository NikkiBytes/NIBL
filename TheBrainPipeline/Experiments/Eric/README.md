## Eric Data

This study contains 4 waves(sessions).

For information on the preprocessing steps please refer to the README_containers.md file

#### LOCATION:

  <b>Main Directory:</b> /projects/niblab/bids_projects/Experiments/EricData <br>
  <b>fMRIprep Data:</b> (session 4)/projects/niblab/bids_projects/Experiments/EricData/fmriprep_session_4 <br>
  <b>BIDS Data:</b> /projects/niblab/bids_projects/Experiments/EricData/EricData




#### DATA DIRECTORY:

**~/fmriprep_run** contains the fmriprep output.
**~/EricData/EricData** contains the BIDS data.
*Note
    -- for task files, under ~/func, there are 2 files for each task,
                the original file, e.g. 'sub-001_task-milkshake_A.json',
                and the motion corrected file, identified with [_physio], e.g. 'sub-001_task-milkshake_A_physio.json'



        ~/Experiments
            /EricData
                /fmriprep_run
                  /sub-001
                    /fmriprep
                      /logs
                      /sub-001
                        /anat
                        /figures
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



### SESSION INFO:

#### Wave 4
      Log Count: 111 | Dicom Count: 98

      Tasks: GoNo1, GoNo2, imagine, milkshakeA, milkshakeB, milkshakeC, milkshakeD

      Subject IDS:
      001  008  018  033  043  049  056  062  071  079  088  094  101  107  116  122  131
      002  011  022  034  044  051  057  063  072  081  089  095  102  109  117  123  132
      004  012  028  037  045  052  058  064  075  082  090  096  103  110  118  126  154
      005  013  029  040  046  053  059  065  076  083  091  097  104  113  119  127
      006  014  030  041  047  054  060  066  077  084  092  098  105  114  120  128
      007  017  032  042  048  055  061  068  078  085  093  099  106  115  121  130

#### *********************************************************************************************************************
