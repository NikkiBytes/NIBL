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
#


fi
