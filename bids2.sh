

# get start variables

get_variables () {
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

bids_process () {

}

main () {
  
}
