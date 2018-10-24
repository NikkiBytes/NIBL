#!/bin/bash



# We move to our study directory, "SugarMama", which contains
# our individual subject directories containing the target dicom ima_files

cd data/SugarMama # MODIFY WITH YOUR UNIQUE INPUT DIRECTORY

# Now we grab an array of our subjects
# if the folder contained only our subject folders we could simply use, (*),
# but here we add the "SM" to specify further our target subjects and ignore
# excess folder in the directory
subjects=(SM*) # MODIFY WITH YOUR UNIQUE SUBJECT FOLDER IDENTIFIER

# We are going to run a parallel process, this divides our subjects into
# 2 different arrays
subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}


# We move back to our main directory
cd /test


# Begin our BIDS Conversion
#parallel process
for f in ${subs1[@]};do
num=$(($num+1))
echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
export f
heudiconv -b -d data/{subject}/${f}/raw/${f}/*/*dcm -s SugarMama -f ConversionFiles/SM_converter.py \
-c dcm2niix -b  -o Experiments/SugarMama/sub-${f}
echo "Finished BIDSifying subject $f"
done &
for f in ${subs2[@]};do
export f
heudiconv -b -d data/{subject}/${f}/raw/${f}/*/*dcm -s SugarMama -f ConversionFiles/SM_converter.py \
-c dcm2niix -b  -o Experiments/SugarMama/sub-${f}
echo "Finished BIDSifying subject $f"
done &
wait
