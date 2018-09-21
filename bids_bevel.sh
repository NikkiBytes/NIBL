
cd /test/raw_data/continuing_studies/Bevel
subjects=(sub*)

subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /test
for f in ${subs1[@]};do
id=${f}
echo $id
echo ">>>>--------> STARTING BIDS CONVERSION ON SUBJECT: $f ...."
echo " INPUT >>>>---------------------------------------> /test/raw_data/continuing_studies/{subject}/$f/*dcm"
export id
heudiconv -b -d  /test/raw_data/continuing_studies/{subject}/$f/*dcm  -s Bevel -f /test/Heuristic_Files/bevel_heuristic.py -c dcm2niix -b  -o /test/Experiments/Bevel/BIDS/$f
echo ">>>>--------> Finished BIDSifying subject $f"
done &
for f in ${subs2[@]};do
echo ">>>>--------> STARTING BIDS CONVERSION ON SUBJECT: $f ...."
echo " INPUT >>>>---------------------------------------> /test/raw_data/continuing_studies/{subject}/session-2/$f/*dcm"
id=${f}
export id
heudiconv -b -d  /test/raw_data/continuing_studies/{subject}/$f/*dcm -s Bevel -f /test/Heuristic_Files/bevel_heuristic.py -c dcm2niix -b  -o /test/Experiments/Bevel/BIDS/$f
echo ">>>>--------> Finished BIDSifying subject $f"
done &
wait
