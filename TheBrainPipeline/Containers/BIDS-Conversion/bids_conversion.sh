#!/bin/bash

read -p "Enter main directory path: " main_directory
read -p "Enter study name: " study_name
read -p "Enter input data path: " input_path # get input path

if [ -z $input_path ]
then
  echo "input path is an empty string"
  #exit
fi

if [ -z $main_directory ]
then
  echo "The main directory is an empty string"
  #exit
fi

if [ ! -e "$main_directory" ]
then
  echo "main directory file path doesn't exist"
#  exit
fi

if [ ! -e "$input_path" ]
then
  echo "input file path doesn't exist"
#  exit
else
  read -p "Enter the subjects identifier[i.e. '*']: " subject_key

  cd $input_path


# Get subjects
  subjects=(${subject_key})

  echo "${subjects[@]}"

  read -p "These are the subjects we found, enter true to proceed:      " decision

  if [ "$decision" = true ] ; then
    echo "Proceeding......"

    subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
    subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

    cd $main_directory

    read -p "Enter heuristic file path: " heuristic_path

    if [ ! -e "$heuristic_path" ]; then
      echo "Heurisitic path doesn't exist"
      exit
    else
      read -p "Enter unique dicom path: " dicom_path
      REPLACE="\{subject\}"
      dcm_path=${dicom_path//$study_name/$REPLACE}

      read -p "Enter output directory path: " output_directory
    fi


    # Start parallel process / Run BIDS
    for f in ${subs1[@]};do
    echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
    id=$(echo $f | cut -f2 -d-)
    export id
    heudiconv -b -d $dcm_path -s $study_name -f $heuristic_path \
    -c dcm2niix -b  -o "$output_directory/sub-${id}"
    echo "Finished BIDSifying subject $f"
    done &
    for f in ${subs2[@]};do
    id=$(echo $f | cut -f2 -d-)
    export id
    heudiconv -b -d $dcm_path -s $study_name -f $heuristic_path \
    -c dcm2niix -b -o "$output_directory/sub-${id}"
    echo "Finished BIDSifying subject $f"
    done &
    wait

  else
    echo "ending"
  fi
fi
