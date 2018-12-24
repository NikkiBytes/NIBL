cd Experiments/EricData/EricData/ses-wave4ls
subject_id=(sub*)
subject_id=({*10*,*11*,*12*,*13*,*15*})
cd /mydirectory

sinteractive -m 24000
singularity shell -B /projects/niblab/bids_projects:/mydirectory Singularity_Containers/fmriprep_container.simg
cd /mydirectory
for i in ${subjects1[@]}; do
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
done
