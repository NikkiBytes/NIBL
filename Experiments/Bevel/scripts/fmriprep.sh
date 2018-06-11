#/bin/bash



cd Experiments/Bevel/Bevel
subjects=(sub*)
subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /mydirectory

echo "Starting fmriprep: " $(date)
START=$(date)
for i in ${subs1[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep Experiments/Bevel/Bevel Experiments/Bevel/$i \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 32 --low-mem \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space T1w --template MNI152NLin2009cAsym \
    --debug \
    -w Experiments/Bevel/$i/intermediate_results --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &

for i in ${subs2[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
<<<<<<< HEAD
fmriprep Experiments/Bevel/Bevel Experiments/Bevel/fmriprep/$i \
=======
fmriprep Experiments/Bevel/Bevel Experiments/Bevel/$i \
>>>>>>> 2ef4d4464265a53bf38ea48664c2cd507a160dbe
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 32 --low-mem \
    --ignore slicetiming  \
    --t2s-coreg --bold2t1w-dof 12 \
    --output-space T1w --template MNI152NLin2009cAsym \
    --debug  \
    -w Experiments/Bevel/$i/intermediate_results --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &
wait

echo "Started fmriprep at: " $START
echo "Finished fmriprep for Bevel at: " $(date -u)
FINISHED=$(date -u)
