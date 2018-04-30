#/bin/bash



cd Experiments/EricData/EricData/ses-wave4
subjects=(sub*)
subs1=${subjects[@]::$((${#subjects[@]} / 2 ))}
subs2=${subjects[@]:$((${#subjects[@]} / 2 ))}

cd /mydirectory


for i in ${subs1[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep Experiments/EricData/EricData/ses-wave4 Experiments/EricData/fmriprep_session_4/$i \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 4 --n_cpus 8 --low-mem \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space T1w --template MNI152NLin2009cAsym \
    --debug --anat-only \
    -w Experiments/EricData/fmriprep_session_4/intermediate_results --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &

for i in ${subs2[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep Experiments/EricData/EricData/ses-wave4 Experiments/EricData/fmriprep_session_4/$i \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 4 --n_cpus 8 --low-mem \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space T1w --template MNI152NLin2009cAsym \
    --debug --anat-only \
    -w Experiments/EricData/fmriprep_session_4/intermediate_results --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &
wait
