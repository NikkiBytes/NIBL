#!/bin/bash
cd Raw_Data/BFClub/sess-v1

subjects=(*)
arr_length=${#subjects[@]}
let "x=$arr_length/3"
subs1=${subjects[@]:0:$x}
subs2=${subjects[@]:$x:$x}
subs3=${subjects[@]:$x+$x}
cd /mydirectory


for sub in ${subs1[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $sub ................................................................"
id=$(echo $sub | cut -f2 -d-)
export id
heudiconv -b -d Raw_Data/{subject}/{session}/$sub/raw/BF*/*/*dcm -s BFClub -ss sess-v1 -f ConversionFiles/bfclub_conversion.py \
-c dcm2niix -b  -o Experiments/BFClub/data/BFClub/${sub}/ses-1
echo "Finished BIDSifying subject $sub"
done &
for sub in ${subs2[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $sub ................................................................"
id=$(echo $sub | cut -f2 -d-)
export id
heudiconv -b -d Raw_Data/{subject}/{session}/$sub/raw/BF*/*/*dcm -s BFClub -ss sess-v1 -f ConversionFiles/bfclub_conversion.py \
-c dcm2niix -b  -o Experiments/BFClub/data/BFClub/${sub}/ses-1
echo "Finished BIDSifying subject $sub"
done &
for sub in ${subs3[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $sub ................................................................"
id=$(echo $sub | cut -f2 -d-)
export id
heudiconv -b -d Raw_Data/{subject}/{session}/$sub/raw/BF*/*/*dcm -s BFClub -ss sess-v1 -f ConversionFiles/bfclub_conversion.py \
-c dcm2niix -b  -o Experiments/BFClub/data/BFClub/${sub}/ses-1
echo "Finished BIDSifying subject $sub"
done &
wait
