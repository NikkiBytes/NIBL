for sub in ${subs[@]}; do
cd /projects/niblab/bids_projects/Experiments/EricData/data/BIDS/EricData/wave3/$sub/func
for f in *ses*; do mv "$f" "${f//ses-2/ses-3}";  done
ls
done 
