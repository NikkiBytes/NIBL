
cd /test/raw_data/finished_studies/ChocoData/wave2/Dicoms/dicoms
subjects=(sub*)

subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /test
for f in ${subs1[@]};do
id=${f}
echo id
echo ">>>>--------> STARTING BIDS CONVERSION ON SUBJECT: $f ...."
export id
heudiconv -b -d  /test/raw_data/finished_studies/{subject}/wave2/Dicoms/dicoms/$f/*dcm -s ChocoData \
-f /test/Heuristic_Files/choco_heuristic.py -c dcm2niix -b  -o /test/Experiments/ChocoData/BIDS/ses-2/$f
echo ">>>>--------> Finished BIDSifying subject $f"
done &
for f in ${subs2[@]};do
echo ">>>>--------> STARTING BIDS CONVERSION ON SUBJECT: $f ...."
id=${f}
export id
heudiconv -b -d  /test/raw_data/finished_studies/{subject}/wave2/Dicoms/dicoms/$f/*dcm -s ChocoData \
-f /test/Heuristic_Files/choco_heuristic.py -c dcm2niix -b  -o /test/Experiments/ChocoData/BIDS/ses-2/$f
echo ">>>>--------> Finished BIDSifying subject $f"
done &
wait


cd /test/raw_data/finished_studies/ChocoData/wave3/Dicoms/dicoms
subjects=(sub*)

subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /test
for f in ${subs1[@]};do
id=${f}
echo id
echo ">>>>--------> STARTING BIDS CONVERSION ON SUBJECT: $f ...."
export id
heudiconv -b -d  /test/raw_data/finished_studies/{subject}/wave3/Dicoms/dicoms/$f/*dcm -s ChocoData \
-f /test/Heuristic_Files/choco_heuristic_w3.py -c dcm2niix -b  -o /test/Experiments/ChocoData/BIDS/ses-3/$f
echo ">>>>--------> Finished BIDSifying subject $f"
done &
for f in ${subs2[@]};do
echo ">>>>--------> STARTING BIDS CONVERSION ON SUBJECT: $f ...."
id=${f}
export id
heudiconv -b -d  /test/raw_data/finished_studies/{subject}/wave3/Dicoms/dicoms/$f/*dcm -s ChocoData \
-f /test/Heuristic_Files/choco_heuristic_w3.py -c dcm2niix -b  -o /test/Experiments/ChocoData/BIDS/ses-3/$f
echo ">>>>--------> Finished BIDSifying subject $f"
done &
wait


cd /test/raw_data/finished_studies/ChocoData/wave4/Dicoms/dicoms
subjects=(sub*)

subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /test
for f in ${subs1[@]};do
id=${f}
echo id
echo ">>>>--------> STARTING BIDS CONVERSION ON SUBJECT: $f ...."
export id
heudiconv -b -d  /test/raw_data/finished_studies/{subject}/wave4/Dicoms/dicoms/$f/*dcm -s ChocoData \
-f /test/Heuristic_Files/choco_heuristic_w4.py -c dcm2niix -b  -o /test/Experiments/ChocoData/BIDS/ses-4/$f
echo ">>>>--------> Finished BIDSifying subject $f"
done &
for f in ${subs2[@]};do
echo ">>>>--------> STARTING BIDS CONVERSION ON SUBJECT: $f ...."
id=${f}
export id
heudiconv -b -d  /test/raw_data/finished_studies/{subject}/wave4/Dicoms/dicoms/$f/*dcm -s ChocoData \
-f /test/Heuristic_Files/choco_heuristic_w4.py -c dcm2niix -b  -o /test/Experiments/ChocoData/BIDS/ses-4/$f
echo ">>>>--------> Finished BIDSifying subject $f"
done &
wait
