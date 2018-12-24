#!/bin/bash
cd Data/Eric_Data/wave3/Dicoms/dicoms

subjects=(*)
subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}
cd /test
for f in ${subs1[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
export f
heudiconv -b -d Data/{subject}/{session}/D*/dicoms/${f}/*dcm -s Eric_Data -ss wave3 -f ConversionFiles/eric_data_conversion.py \
-c dcm2niix -b  -o Experiments/EricData/EricData/ses-wave3/sub-${f}
echo "Finished BIDSifying subject $f"
done &
for f in ${subs2[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
export f
heudiconv -b -d Data/{subject}/{session}/D*/dicoms/${f}/*dcm -s Eric_Data -ss wave3 -f ConversionFiles/eric_data_conversion.py \
-c dcm2niix -b  -o Experiments/EricData/EricData/ses-wave3/sub-${f}
echo "Finished BIDSifying subject $f"
done &
wait
