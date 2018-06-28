for sub in ${subs[@]}; do
cd /projects/niblab/bids_projects/Experiments/EricData/data/BIDS/EricData/wave3/$sub/func
for f in *ses*; do mv "$f" "${f//ses-2/ses-3}";  done
ls
done


subs=(sub-*)
for i in ${subs[@]}; do
    sub=$(echo $i | cut -f1 -d_)
    mv $i /projects/niblab/bids_projects/Experiments/Bevel/data/derivatives/$sub/func/onsets
done

for sub in ${subs[@]}; do
  cd /projects/niblab/bids_projects/Raw_Data/Eric_Data/wave2
  while IFS=" " read -r val1 val2
  do
  mv $val1 "sub-$val2"
done < "EricData.txt"
