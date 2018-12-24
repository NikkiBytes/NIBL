#!/bin/bash

cd Data/Eric_Data/wave1/dicoms
subjects=(*)
subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /test/Data/Eric_Data/wave1/ima_files
ima_subs=(*)



cd /test
for f in ${subs1[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
export f
heudiconv -b -d Data/{subject}/{session}/dicoms/${f}/*dcm -s Eric_Data -ss wave1 -f ConversionFiles/eric_data_conversion.py \
-c dcm2niix -b  -o Experiments/EricData/EricData/ses-wave1/sub-${f}
echo "Finished BIDSifying subject $f"
done &
for f in ${subs2[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
export f
heudiconv -b -d Data/{subject}/{session}/dicoms/${f}/*dcm -s Eric_Data -ss wave1 -f ConversionFiles/eric_data_conversion.py \
-c dcm2niix -b  -o Experiments/EricData/EricData/ses-wave1/sub-${f}
echo "Finished BIDSifying subject $f"
done &
for f in ${ima_subs[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
export f
heudiconv -b -d Data/{subject}/{session}/dicoms/${f}/*IMA-s Eric_Data -ss wave1 -f ConversionFiles/eric_data_conversion.py \
-c dcm2niix -b  -o Experiments/EricData/EricData/ses-wave1/sub-${f}
echo "Finished BIDSifying subject $f"
done &
wait
