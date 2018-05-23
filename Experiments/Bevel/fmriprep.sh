#/bin/bash



cd Experiments/Bevel/Bevel
subjects=(sub*)
arr_length=${#subjects[@]}
let "x=$arr_length/3"
subs1=${subjects[@]:0:$x}
subs2=${subjects[@]:$x:$x}
subs3=${subjects[@]:$x+$x}
cd /mydirectory

echo "Starting fmriprep: " $(date)
START=$(date)
for i in ${subs1[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep Experiments/Bevel/Bevell Experiments/Bevel/fmriprep_new/$i \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 32 \
    --ignore slicetiming  \
    --t2s-coreg --bold2t1w-dof 12 \
    --output-space T1w --template MNI152NLin2009cAsym \
    --debug \
    -w Experiments/Bevel/fmriprep_new/$i/intermediate_results \
    --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &

for i in ${subs2[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)

fmriprep Experiments/Bevel/Bevell Experiments/Bevel/fmriprep_new/$i  \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 32 \
    --ignore slicetiming  \
    --t2s-coreg --bold2t1w-dof 12 \
    --output-space T1w --template MNI152NLin2009cAsym \
    --debug  \
    -w Experiments/Bevel/fmriprep_new/$i/intermediate_results \
    --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &

for i in ${subs3[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)

fmriprep Experiments/Bevel/Bevell Experiments/Bevel/fmriprep_new/$i  \
    participant  \
    --participant-label $i  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 32 \
    --ignore slicetiming  \
    --t2s-coreg --bold2t1w-dof 12 \
    --output-space T1w --template MNI152NLin2009cAsym \
    --debug  \
    -w Experiments/Bevel/fmriprep_new/$i/intermediate_results \
    --resource-monitor --write-graph --stop-on-first-crash

echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done &
wait

echo "Started fmriprep at: " $START
echo "Finished fmriprep for Bevel at: " $(date -u)
FINISHED=$(date -u)
