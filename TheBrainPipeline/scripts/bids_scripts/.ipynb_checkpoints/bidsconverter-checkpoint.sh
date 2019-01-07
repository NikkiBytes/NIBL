#!/bin/bash

# @author: Nichollette Acosta
# @position: Data analyst for NIBL at UNC Chapel Hill
# @title: BIDS Conversion

# This is an automated script for running a BIDS conversion on raw fMRI data (dicom, IMA, (etc?))
# There are a few assumptions made in the script:
# -- The subjects have been renamed to the 'sub*' format, *see 'rename_subjects.sh',
# -- that you are running the script within the Heudiconv singularity shell,
# -- and that you have an available heurisitic file for your data, see 'heuristic_file.py'




#********************************************************************************************************
# BEGIN PROGRAM

# Get start variables:
#_____________________

# main directory path is the 'head' directory, this must contain deeper paths to the input data, output
# folder, and the heuristic file.
read -p "Enter main directory path: " MAINDIR

# the study name is the title of the experiment and must be identical to the study name found in the
# dicom path
read -p "Enter study name: " STUDYNAME

# the input path must be the directory path that holds the subject folders (may be the same as MAINDIR)
read -p "Enter input data path: " INPUTDIR

# the output path is the directory where the BIDS subject folders will be written to
read -p "Enter output directory path: " OUTPUTDIR


# Check variables:
#_________________

# Get subjects from input folder:
#_______________________________

# move to input directory
cd $INPUTDIR
# grab the subje
subjects=(sub*)

# confirm subjects and proceed
echo "HERE ARE THE SUBJECTS FOUND:  ${subjects[@]}"
read -p "Proceed with conversion?(enter true):  " CONTINUE

# CHECK CONTINUE VARIABLE

# If true, start BIDS process --
if ["$CONTINUE" = true ] ; then
  echo "Proceeding..........."


# split subjects into 2 different arrays
  subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
  subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

# change to main, "top level", directory
  cd $MAINDIR

# get heuristic file path
  read -p "Enter heuristic file path: " HEURISTICPATH

# check if heuristic file path exists -- cannot continue if unavailable
  if [ ! -e "$HEURISTICPATH" ]; then
    echo "Heurisitic path doesn't exist"
    exit
  else
# if heuristic path exists get dicom path
read -p "$(echo -e 'Please enter the dicom path \n***Enter sub* in placement of the sub-X and *dcm/*IMA for the raw data*** \nEnter Path: ' )"  DCMPATH
    # replace the subject name with the required subject expression for the heudiconv converter
    REPLACE="{subject}"
    DCMPATH=${DCMPATH//$STUDYNAME/$REPLACE}


    # Start parallel process, run BIDS
    for f in ${subs1[@]};do
    echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
    id=$(echo $f | cut -f2 -d-)
    export id
    heudiconv -b -d $DCMPATH -s $STUDYNAME -f $HEURISTICPATH \
    -c dcm2niix -b  -o "$OUTPUTDIR/sub-${id}"
    echo "Finished BIDSifying subject $f"
    done &
    for f in ${subs2[@]};do
    id=$(echo $f | cut -f2 -d-)
    export id
    heudiconv -b -d $DCMPATH -s $STUDYNAME -f $HEURISTICPATH \
    -c dcm2niix -b  -o "$OUTPUTDIR/sub-${id}"
    echo "Finished BIDSifying subject $f"
    done &
    wait
