## Bevel Experiment

For information on the preprocessing steps please refer to the < > file.

Summary:                   
537 Files, 3.23GB                                           
18 - Subjects                                                 
1 - Session                                      

Available Tasks: prob, rest<br>
Available Modalities: T1w, bold, fieldmap

#### LOCATION:

  <b>Main Directory:</b>     /projects/niblab/bids_projects/Experiments/Bevel <br>
  <b>fMRIprep Data:</b>     /projects/niblab/bids_projects/Experiments/Bevel/data/fmriprep <br>
  <b>BIDS Data:</b>         /projects/niblab/bids_projects/Experiments/Bevel/data/Bevel


#### DATA DIRECTORY

  /projects/niblab/bids_projects/Experiments/Bevel/data/Bevel

      Bevel/
        dataset_description.json
        sub-001_scans.tsv
        task-prob_bold.json
        task-rest_bold.json
        sub-001/
          anat/
            sub-001_T1w.json  
            sub-001_T1w.nii.gz
          func/
            sub-001_task-rest_bold.json
            sub-001_task-rest_bold.nii.gz
            sub-001_task-rest_events.tsv
            sub-001_task-prob_run-1{2,3,4}_bold.json
            sub-001_task-prob_run-1{2,3,4}_bold.nii.gz
            sub-001_task-prob_run-1{2,3,4}_events.tsv
          fmap/
            sub-001_magnitude1.json    
            sub-001_magnitude2.json    
            sub-001_phasediff.json
            sub-001_magnitude1.nii.gz  
            sub-001_magnitude2.nii.gz  
            sub-001_phasediff.nii.gz

  /projects/niblab/bids_projects/Experiments/Bevel/data/fmriprep

    fmriprep/
      sub-001/
        fmriprep/
          logs/
          sub-001/
            anat/
            figures/
            func/
          sub-001.html
        intermediate_results/
          fmriprep_wf/
            d3.js  
            graph1.json  
            graph.dot  
            graph.json  
            graph.svg  
            index.html  
            single_subject_001_wf/
              about/
              bidssrc/            
              func_preproc_task_prob_run_1_wf/
              func_preproc_task_prob_run_2_wf/
              func_preproc_task_prob_run_3_wf/   
              func_preproc_task_prob_run_4_wf/
              anat_preproc_wf/  
              ds_report_about/    
              func_preproc_task_rest_wf/
              bids_info/        
              ds_report_summary/  
              summary/
          reportlets/
            fmriprep/
              sub-001/
                anat/
                func/
