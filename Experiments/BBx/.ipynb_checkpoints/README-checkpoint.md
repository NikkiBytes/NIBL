Study: BBx
Date: Fall 2018 


derivatives/ 
    quality_ana/        -- this holds the quality analysis reports 
    design_files/       -- this holds the design file templates for feat analysis (labeled according to level)
    group_ana/          -- this holds feat 3 analysis directories and fsf files or group analysis
    sub-XXX/            -- this holds the individual subject data, divided by ses-1 and ses-2 
        ses-X/
            anat/               -- this holds the anatomical file for the corresponding subject
            func/               -- this holds the functional files for the corresponding subject and other relevant directories
                Analysis/           -- this holds the feat 1 and feat 2 directories 
                    feat1/              -- this holds the feat 1 fsf files and directories made from analysis
                    feat2/              -- this holds the feat 2 fsf files and directories made from analysis
                motion_assessment/  -- this holds our confound files and the directory that holds the motion parameters
                    motion_parameters/  -- this holds the motion parameter (.txt) files 
                onsets/             -- this holds the onset files
                
              
Preprocessing Information: 

I.      BIDS Conversion
II.     FMRIPREP        -- parameters used {}
III.    FSL Feat 1      -- parameters used {}
IV.     FSL Feat 2      -- parameters used {}
V.      FSL Feat 3      -- parameters used {}