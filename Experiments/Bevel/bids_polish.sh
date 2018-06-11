read -p "Enter main directory path: " main_directory
(echo -e "participant_id \t age \t sex") | column -t >> participants.tsv
cd $main_directory
subjects=(sub*)

for sub in ${subjects[@]}; do
    cd $sub
    info=$(awk 'NR == 2 {print "\t" $2 "\t" $3}' participants.tsv)
    echo $info
    cd $main_directory
    echo "$sub  $info" >> participants.tsv
done

for sub in ${subjects[@]}; do
  cd $sub
  rm CHANGES README participants.tsv dataset_description.json
  cd $main_directory
done
