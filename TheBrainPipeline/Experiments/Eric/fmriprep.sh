#/bin/bash



cd /home_dir/Experiments/ChocoData/BIDS/ses-2

subjects=(sub*)
arr_length=${#subjects[@]}
let "x=$arr_length/3"
subs1=${subjects[@]:0:$x}
subs2=${subjects[@]:$x:$x}
subs3=${subjects[@]:$x+$x}
cd /home_dir



echo "Starting fmriprep: " $(date)
START=$(date)

for i in ${subs1[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep /home_dir/Experiments/ChocoData/BIDS/ses-2 /home_dir/Experiments/ChocoData/fmriprep/$i/ses-2 \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 15 --n_cpus 30  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug  \
    -w /home_dir/Experiments/ChocoData/fmriprep/$i/ses-2  \
    --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &
for i in ${subs2[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep /home_dir/Experiments/ChocoData/BIDS/ses-2 /home_dir/Experiments/ChocoData/fmriprep/$i/ses-2 \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 15 --n_cpus 30  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug  \
    -w /home_dir/Experiments/ChocoData/fmriprep/$i/ses-2  \
    --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &
for i in ${subs3[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep /home_dir/Experiments/ChocoData/BIDS/ses-2 /home_dir/Experiments/ChocoData/fmriprep/$i/ses-2 \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 15 --n_cpus 30  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug  \
    -w /home_dir/Experiments/ChocoData/fmriprep/$i/ses-2  \
    --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &
wait

echo "Started fmriprep at: " $START
echo "Finished fmriprep for CHOCOLATE at: " $(date -u)
FINISHED=$(date -u)
exit
exit
exit
