

# get start variables

get_start_variables () {
# main directory path is the 'head' directory, this must contain deeper paths to the input data, output
# folder, and the heuristic file.
  read -p "Enter main directory path: " MAINDIR
  if [ -z $MAINDIR ]
  then
    echo "input path is an empty string"
  fi
  if [ ! -e $MAINDIR]
  then
    echo "Main directory doesn't exist"
  fi


# the study name is the title of the experiment and must be identical to the study name found in the
# dicom path
  read -p "Enter study name: " STUDYNAME
  if [ -z $STUDYNAME ]
  then
    echo "input path is an empty string"
  fi


# the input path must be the directory path that holds the subject folders (may be the same as MAINDIR)
  read -p "Enter input data path: " INPUTDIR
  if [ -z $INPUTDIR ]
  then
    echo "input path is an empty string"
  fi
  if [ ! -e $INPUTDIR ]
  then
    echo "INPUT IS AN EMPTY STRING"
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
  echo "HERE ARE THE SUBJECTS FOUND:  ${subjects[@]}"
  # confirm subjects from user
  read -p "Proceed with conversion?(enter true):  " CONTINUE
}

get_bids_variables () {
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
}

# Start parallel process / Run BIDS
bids_process () {
  for sub1 in ${subs1[@]};do
  echo "STARTING BIDS CONVERSION ON SUBJECT: $sub1 ................................................................"
  id=$(echo $sub1 | cut -f2 -d-)
  export id
  heudiconv -b -d $DCMPATH -s $STUDYNAME -f $HEURISTICPATH \
  -c dcm2niix -b  -o "$OUTPUTDIR/sub-${id}"
  echo "Finished BIDSifying subject $sub2"
  done &
  for sub2 in ${subs2[@]};do
  echo "STARTING BIDS CONVERSION ON SUBJECT: $sub2 ................................................................"
  id=$(echo $sub2 | cut -f2 -d-)
  export id
  heudiconv -b -d $DCMPATH -s $STUDYNAME -f $HEURISTICPATH \
  -c dcm2niix -b  -o "$OUTPUTDIR/sub-${id}"
  echo "Finished BIDSifying subject $sub2"
  done &
  wait
}

main () {
  get_start_variables
  get_subjects $INPUTDIR

  if ["$CONTINUE" = true ] ; then
    bids_process
  else
    echo "SUBJECTS WERE DECLARED FALSE, EXITING..................................."
  fi
}
