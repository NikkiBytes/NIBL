cd /projects/niblab/bids_projects/Experiments/EricData/EricData/ses-wave4
subs=(sub*)
for sub in ${subs[@]}; do
cd $sub/func
for f in *.json; do mv "$f" "${f%.json}_bold.json"; done
for f in *.nii.gz; do mv "$f" "${f%.nii.gz}_bold.nii.gz"; done
ls
cd /projects/niblab/bids_projects/Experiments/EricData/EricData/ses-wave4
