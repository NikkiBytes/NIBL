#/bin/bash



cd /home_dir/Experiments/Bevel/BIDS
subjects=(sub*)
subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /home_dir

echo "Starting fmriprep: " $(date)
START=$(date)
for i in ${subs1[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep /home_dir/Experiments/Bevel/BIDS /home_dir/Experiments/Bevel/fmriprep/$i \
    participant  \
    --participant-label $id  \
    --fs-license-file /home_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 8 --n_cpus 16 --low-mem \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug \
    -w /home_dir/Experiments/Bevel/fmriprep/$i \
    --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &

for i in ${subs2[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep /home_dir/Experiments/Bevel/BIDS /home_dir/Experiments/Bevel/fmriprep/$i \
    participant  \
    --participant-label $id  \
    --fs-license-file /home_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 8 --n_cpus 16 --low-mem \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug \
    -w /home_dir/Experiments/Bevel/fmriprep/$i \
    --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &
wait

echo "Started fmriprep at: " $START
echo "Finished fmriprep for Bevel at: " $(date -u)
FINISHED=$(date -u)
