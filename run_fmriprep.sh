cd Experiments/EricData/EricData/ses-wave4
subject_id=(sub*)
subject_id=({*-07*,*-08*,*-09*,*10*,*11*,*12*,*13*,*15*})
cd /mydirectory

sinteractive -m 24000
singularity shell -B /projects/niblab/bids_projects:/mydirectory \
 /projects/niblab/bids_projects/Singularity_Containers/fmriprep_container.simg
cd /mydirectory
for i in ${subject_id[@]}; do
echo "Starting fmriprep for subject $i..................................................."
id=$(echo $i | cut -f2 -d-)
fmriprep Experiments/EricData/EricData/ses-wave4 Experiments/EricData/fmriprep_run/$i \
    participant  \
    --participant-label $id  \
    --fs-license-file freesurfer/license.txt \
    --omp-nthreads 4 --n_cpus 8  --low-mem \
    --ignore slicetiming  \
    --output-space T1w --template MNI152NLin2009cAsym \
    --fs-no-reconall --debug --anat-only \
    -w intermediate_results --resource-monitor --write-graph --stop-on-first-crash


echo "...................................................finished fmriprep for subject $i"
echo "********************************************************************************************"
done
