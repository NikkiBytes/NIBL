subs=(sub-*)
for i in ${subs[@]}; do
    sub=$(echo $i | cut -f1 -d_)
    mv $i /projects/niblab/bids_projects/Experiments/Bevel/data/derivatives/$sub/func/onsets
done
