#/bin/bash



cd /home_dir/Experiments/bbx/BIDS/ses-1
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
echo ">>>>>>------------------------------------>STARTING FMRIPREP ON SUBJECT $i"
id=$(echo $i | cut -f2 -d-)
fmriprep /home_dir/Experiments/bbx/BIDS/ses-1 /home_dir/Experiments/bbx/fmriprep/ses-1/$i \
    participant  \
    --participant-label $id  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 8 --n_cpus 16 \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug  --ignore slicetiming \
    -w Experiments/bbx/fmriprep/$i/ses \
    --resource-monitor --write-graph --stop-on-first-crash

echo ">>>>>>------------------------------------>FINISHING FMRIPREP FOR SUBJECT $i"
echo "********************************************************************************************"
done &
for i in ${subs2[@]}; do
echo ">>>>>>------------------------------------>STARTING FMRIPREP ON SUBJECT $i"
id=$(echo $i | cut -f2 -d-)
fmriprep /home_dir/Experiments/bbx/BIDS/ses-1 Experiments/bbx/fmriprep/ses-1/$i \
    participant  \
    --participant-label $id  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 8 --n_cpus 16 \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug  --ignore slicetiming \
    -w Experiments/bbx/fmriprep/ses-1/$i \
    --resource-monitor --write-graph --stop-on-first-crash


echo ">>>>>>------------------------------------>FINISHING FMRIPREP FOR SUBJECT $i"
echo "********************************************************************************************"
done &
for i in ${subs3[@]}; do
echo ">>>>>>------------------------------------>STARTING FMRIPREP ON SUBJECT $i"
id=$(echo $i | cut -f2 -d-)
fmriprep /home_dir/Experiments/bbx/BIDS/ses-1 Experiments/bbx/fmriprep/ses-1/$i \
    participant  \
    --participant-label $id  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 8 --n_cpus 16 \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug  --ignore slicetiming \
    -w Experiments/bbx/fmriprep/ses-1/$i \
    --resource-monitor --write-graph --stop-on-first-crash


echo ">>>>>>------------------------------------>FINISHING FMRIPREP FOR SUBJECT $i"
echo "********************************************************************************************"
done &
wait

echo "Started fmriprep at: " $START
echo "Finished fmriprep for BBx at: " $(date -u)
FINISHED=$(date -u)
exit
exit
