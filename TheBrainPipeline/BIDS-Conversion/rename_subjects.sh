#!/bin/bash

# This script changes subject names to "sub-XXX" while recording the original.


read -p "Enter path: " path # get input path


if [ -z $path ]
then
  echo "path is an empty string"
  exit
fi

if [ ! -e "$path" ]
thenssh
  echo "file path doesn't exist"
else
  echo "Starting Program:"ls
  cd $path # go to input path

  read -p "Enter Experiment Name: " experiment

  read -p "Enter subject keyword: " keyword

  subjects=(${keyword})

  count=0

  for sub in ${subjects[@]}; do
    count=$((count+1))
    subj_num=`printf "%03d" $count`
    new_sub="sub-$subj_num"
    echo -e "$new_sub \t $sub" >> $experiment.txt
    mv $sub $new_sub
    echo ".............................................................."
  done
fi
