
cd Data/Bevel
subjects=(sub*)

subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /test
for f in ${subs1[@]};do
id=$(echo $f | cut -f2 -d-)
echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
export id
heudiconv -b -d Raw_Data/{subject}/$f/*dcm -s BBx -f ConversionFiles/bevel_converter.py \
-c dcm2niix -b  -o Experiments/Bevel/Bevel/$f
echo "Finished BIDSifying subject $f"
done &
for f in ${subs2[@]};do
echo "STARTING BIDS CONVERSION ON SUBJECT: $f ................................................................"
id=$(echo $f | cut -f2 -d-)
export id
heudiconv -b -d Raw_Data/{subject}/$f/*dcm -s BBx -f ConversionFiles/bevel_converter.py \
-c dcm2niix -b  -o Experiments/Bevel/Bevell/$f
echo "Finished BIDSifying subject $f"
done &
wait
