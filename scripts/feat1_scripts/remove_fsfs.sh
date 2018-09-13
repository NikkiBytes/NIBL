for sub in ${subs[@]}; do
cd /projects/niblab/bids_projects/Experiments/BBx/derivatives/$sub/ses-1/func/Analysis
rm *.fsf
cd /projects/niblab/bids_projects/Experiments/BBx/derivatives
done
cd /projects/niblab/bids_projects/Experiments/Bevel/data/derivatives

for sub in ${subs[@]}; do
cd /projects/niblab/bids_projects/Experiments/BBx/derivatives/$sub/ses-1/func/Analysis/feat1
rm -rf run*.feat
cd /projects/niblab/bids_projects/Experiments/BBx/derivatives
done
