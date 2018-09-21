#/bin/bash

# @Author: Nichollette Acosta
# BIDS conversion automation scripts made for NIBL at Chapel Hill

# get start variables
get_start_variables () {
# main directory path is the 'head' directory, this must contain deeper paths to the input data, output
# folder, and the heuristic file.
  #read -p "Enter main directory path: " MAINDIR
  #if [ -z $MAINDIR ]
  #then
  #  echo "input path is an empty string"
  #fi
  #if [ ! -e $MAINDIR]
  #then
  #  echo "Main directory doesn't exist"
  #fi
  MAINDIR='/test'
  read -p "Is this a multi-session study?(Enter true): " MULTISESS
  if [ "$MULTISESS" = true ]; then
    read -p "Enter session: " SESSION
  fi



# the study name is the title of the experiment and must be identical to the study name found in the
# dicom path
  read -p "Enter study name: " STUDYNAME
  if [ -z $STUDYNAME ]
  then
    echo "INPUT IS AN EMPTY STRING"
  fi


# the input path must be the directory path that holds the subject folders (may be the same as MAINDIR)
  read -p "Enter input data path: " INPUTDIR
  if [ -z $INPUTDIR ]
  then
    echo "INPUT IS AN EMPTY STRING"
  fi
  if [ ! -e $INPUTDIR ]
  then
    echo "INPUT DIRECTORY DOES NOT EXIST"
  fi


# the output path is the directory where the BIDS subject folders will be written to
  read -p "Enter output directory path: " OUTPUTDIR

}


get_subjects () {
  # move to input directory
  cd $INPUTDIR
  # grab the subjects
  subjects=(sub*)

  # display subjects found
  echo -e  "HERE ARE THE SUBJECTS FOUND:  \n ${subjects[@]}"
  # confirm subjects from user
  read -p "Proceed with conversion?(Enter true):  " CONTINUE
  cd $MAINDIR
}

get_bids_variables () {
  read -p "Enter heuristic file path: " HEURISTICPATH
  # check if heuristic file path exists -- cannot continue if unavailable
  if [ ! -e "$HEURISTICPATH" ]; then
    echo "Heurisitic path doesn't exist"
    exit
  else
    if [ "$MULTISESS" = true ]; then
      read -p "$(echo -e 'Read carefully to input the dicom path. \n***Enter sub* in placement of the sub-X and *dcm/*IMA for the raw data*** \nEnter Path: ' )"  DCMPATH
      REPLACESUB='{subject}'
      DCMPATH="${DCMPATH//$STUDYNAME/$REPLACESUB}"
      REPLACESES='{session}'
      DCMPATH="${DCMPATH//$SESSION/$REPLACESES}"
      echo "DICOM PATH: ${DCMPATH}"
    else
   # if heuristic path exists get dicom path
      read -p "$(echo -e 'Please enter the dicom path \n***Enter sub* in placement of the sub-X and *dcm/*IMA for the raw data*** \nEnter Path: ' )"  DCMPATH
      # replace the subject name with the required subject expression for the heudiconv converter
      REPLACE='{subject}'
      DCMPATH=${DCMPATH//$STUDYNAME/$REPLACE}
      echo "DICOM PATH: ${DCMPATH}"
    fi
  fi
}

# Start parallel process / Run BIDS
bids_process () {
#seperate subjects for parallel processing
  subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
  subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}
# run multi session BIDS conversion
  if [ "$MULTISESS" = true ] ;
  then
    for sub1 in ${subs1[@]};do
      DCMPATH=${DCMPATH//'sub*'/$sub1}
      echo "STARTING MULTI-SESS BIDS CONVERSION ON SUBJECT $sub1 ................................................................"
      echo "_____________________________________________________________________________________________________________________"
      echo "${id}"
      id=$(echo $sub1 | cut -f2 -d-)
      export id
      heudiconv -b -d $DCMPATH -s $STUDYNAME -ss $SESSION -f $HEURISTICPATH \
      -c dcm2niix -b  -o "$OUTPUTDIR/sub-${id}"
      echo "_____________________________________________________________________________________________________________________"
      echo "COMPLETED BIDS CONVERSION FOR SUBJECT $sub1"
    done &
    for sub2 in ${subs2[@]};do
      DCMPATH=${DCMPATH//'sub*'/$sub2}
      echo "STARTING MULTI-SESS BIDS CONVERSION ON SUBJECT $sub2 ................................................................"
      echo "_____________________________________________________________________________________________________________________"
      id=$(echo $sub2 | cut -f2 -d-)
      export id
      heudiconv -b -d $DCMPATH -s $STUDYNAME -ss $SESSION -f $HEURISTICPATH  \
      -c dcm2niix -b  -o "$OUTPUTDIR/sub-${id}"
      echo "_____________________________________________________________________________________________________________________"
      echo "COMPLETED BIDS CONVERSION FOR SUBJECT $sub2"
    done &
    wait
# run single session BIDS
  else
    for sub1 in ${subs1[@]};do
      DCMPATH=${DCMPATH//'sub*'/$sub1}
      echo "STARTING BIDS CONVERSION ON SUBJECT $sub1 ................................................................"
      echo "__________________________________________________________________________________________________________"
      id=$(echo $sub1 | cut -f2 -d-)
      export id
      heudiconv -b -d $DCMPATH -s $STUDYNAME -f $HEURISTICPATH \
      -c dcm2niix -b  -o "$OUTPUTDIR/sub-${id}"
      echo "__________________________________________________________________________________________________________"
      echo "COMPLETED BIDS CONVERSION FOR SUBJECT $sub1"
    done &
    for sub2 in ${subs2[@]};do
      DCMPATH=${DCMPATH//'sub*'/$sub2}
      echo "STARTING BIDS CONVERSION ON SUBJECT $sub2 ................................................................"
      echo "__________________________________________________________________________________________________________"
      id=$(echo $sub2 | cut -f2 -d-)
      export id
      heudiconv -b -d $DCMPATH -s $STUDYNAME -f $HEURISTICPATH  \
      -c dcm2niix -b  -o "$OUTPUTDIR/sub-${id}"
      echo "__________________________________________________________________________________________________________"
      echo "COMPLETED BIDS CONVERSION FOR SUBJECT $sub2"
    done &
    wait
  fi
}

main () {
  #get start variables
  get_start_variables
  #get subjects get confirmation
  get_subjects

  #if subjects are confirmed continue with process/ else exit
  if [ "$CONTINUE" = true ] ; then
    get_bids_variables
    bids_process
  else
    echo "SUBJECTS WERE DECLARED FALSE, EXITING..................................."
    exit
  fi
}
