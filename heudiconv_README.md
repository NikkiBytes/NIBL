## BIDS conversion with Heudiconv 

### Workflow
Log into HPC --> Start Singularity shell --> Validate BIDS dataset

    Heudiconv Command
      heudiconv heudiconv -d {input_dir} -s {subject} -ss {session} -f {conversion_files} -c dcm2niix -o {output_directory}
  
  
  
