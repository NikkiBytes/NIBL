### Running Singularity Containers
This README contains details for the currently available Singularity containers for fMRI data prep.

Log into RENCI:

        $ ssh -XY your_account@ht4.renci.org
        $ {your_password}


Singularity Containers are located in the ~/Singularity_Containers folder:

        $ cd /projects/niblab/bids_projects/Singularity_Containers


To run Singularity Containers:

      There are various ways to run the singularity container, for the labs purpose I've currently been using an interactive shell,<br>
      this gives us access to the environment within the container we have created and flexibility in testing and executing our commands.



      Before running any singularity commands we have to run the sinteractive shell:

          $ sinteractive


      Here is the main template of running the singularity shell. See how we use the '-B' flag to bind our data directory to the containers directory.<br>
      Without this we will not have access to our directories. Note that the container directory has been defined during the containers development and <br>
      is unique for each container.  

          $ singularity shell -B {our_directory}:{container_directory} {image}



      Available Containers and their container directory:

              - heudiconv.simg                /test
              - bids_validator                /test
              - fmriprep_container.simg       /mydirectory


Examples:

BIDS Converter with Heudiconv <br>
  Image: heudiconv.simg

          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/heudiconv.simg
          $ cd /test



BIDS Validator <br>
  Image: bids_validator.simg

          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/bids_validator.simg
          $ cd /test



fMRI Prep<br>
  Image: fmriprep_container.simg

          $ cd /projects/niblab/bids_projects
          $ sinteractive
          $ singularity shell -B /projects/niblab/bids_projects:/mydirectory Singularity_Containers/fmriprep_container.simg
          $ cd /mydirectory
