cd /projects/niblab/bids_projects/Raw_Data/Bevel/onsets/bids_ready

subs =(sub*)

for f in ${subs[@]}; do
  var1=$(echo $f | cut -f1 -d_)
  var3=$(echo $f | cut -f3 -d_)
  run=$(echo $var3 | cut -f1 -d.)
  mv $f /projects/niblab/bids_projects/Experiments/Bevel/Bevel/$var1/func/${var1}_task-prob_${run}_events.tsv
done
