
fmriprep /home_dir/Experiments/BBx/BIDS/ses-1 Experiments/bbx/fmriprep/ses-1/$id \
    participant  \
    --participant-label $id  \
    --fs-license-file freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 8 --n_cpus 16 \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug  --ignore slicetiming \
    -w Experiments/bbx/fmriprep/ses-1/$id \
    --resource-monitor --write-graph --stop-on-first-crash
