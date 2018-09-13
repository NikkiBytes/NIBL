
files=(*.txt)

for f in ${files[@]}; do
id=$(echo $f | cut -f1 -d_)
id2=$(echo $id | cut -f2 -dl)
mkdir /projects/niblab/bids_projects/Experiments/Bevel/data/derivatives/sub-0${id2}/onsets
mv $f /projects/niblab/bids_projects/Experiments/Bevel/data/derivatives/sub-0${id2}/onsets

done
