#!/bin/bash

read -p "Enter main directory path: " main_directory

read -p "Enter input data path: " input_path # get input path

if [ -z $input_path ]
then
  echo "input path is an empty string"
  exit
fi

if [ -z $main_directory ]
then
  echo "main_directory is an empty string"
  exit
fi

if [ -e "$main_directory" ]
then
  echo "main directory file path doesn't exist"
  exit
fi

if [ -e "$input_path" ]
then
  echo "file path doesn't exist"
  exit
else
  read -p "Enter the subjects identifier[i.e. '*']: " subject_key
  cd $input_path

# Get subjects
  subjects=($subject_key)
# Divide subjects
  subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
  subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}


  cd $main_directory


# Get conversion file directory
  read -p "Enter heuristic file path: " heuristic_path
  read -p "Enter unique dicom path: " dicom_path
  read -p "Enter study name: " study_name
  read -p "Enter output directory path: " output_directory

  if [ -e "$heuristic_path" ]
  then
    echo "heuristic file path doesn't exist"
    exit
  fi


  # Begin our BIDS Conversion
  #parallel process
  for f in ${subs1[@]};do
  echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
  id=$(echo $i | cut -f2 -d-)
  export f
  heudiconv -b -d $dicom_path -s $study_name -f $heuristic_path \
  -c dcm2niix -b  -o "$output_directory/sub-${id}"
  echo "Finished BIDSifying subject $f"
  done &
  for f in ${subs2[@]};do
  export f
  heudiconv -b -d data/{subject}/${f}/raw/${f}/*/*dcm -s SugarMama -f ConversionFiles/SM_converter.py \
  -c dcm2niix -b  -o Experiments/SugarMama/sub-${f}
  echo "Finished BIDSifying subject $f"
  done &
  wait
