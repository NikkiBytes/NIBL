read -p "Enter main directory path: " main_directory

cd $main_directory
subjects=(sub*)

for sub in ${subjects[@]}; do
    cd $sub
    info=$(awk 'NR == 2 {print "\t" $2 "\t" $3}' participants.tsv)
    newLine="${sub}${info}"
    echo $newLine
    cd $main_directory
done
