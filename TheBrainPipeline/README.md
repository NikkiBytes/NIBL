# File Structure  
<br>
<br>  

    bids/    
      sourcedata/     
      derivatives/  
        fmriprep/
        sub-XX/[ses-X]
          anat/
          func/
            [sub-XX_ses-X_task]-preproc_bold_brain.nii.gz  
            [sub-XX_ses-X_task]-preproc_bold_brain_mask.nii.gz
            [sub-XX_ses-X_task]-preproc_bold.nii.gz
            motion_assessment/
              [sub-XX_ses-X_task]-preproc_brain_confound.txt
              [sub-XX_ses-X_task]-preproc_brain_outlier_output.txt
              [run-X_]fd_plot.png
              motion_parameters/
                [task-X_run-X_]moco[0-5].txt
