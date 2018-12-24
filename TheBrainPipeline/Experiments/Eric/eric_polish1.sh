
# Here I am adjusting sessions around to meet complete BIDS format and get rid of excess files


# We grab our session subjects
session=(ses-wave2 ses-wave1 ses-wave3 ses-wave4)


for sess in ${session[@]};
do
cd /projects/niblab/bids_projects/Experiments/EricData/EricData/$sess
subjects=(sub*)
cd /projects/niblab/bids_projects/Experiments/EricData/EricData
for subj in ${subjects[@]};
do
echo "Checking for directory"
mkdir -p $subj
cd $subj
mkdir -p $sess
cd /projects/niblab/bids_projects/Experiments/EricData/EricData/$sess/$subj
mv  -v anat func fmap "${subj}_scans.tsv" participants.tsv /projects/niblab/bids_projects/Experiments/EricData/EricData/$subj/$sess
echo "Moved subject: $subj"
cd /projects/niblab/bids_projects/Experiments/EricData/EricData
done
echo "Moving onto Session: $sess "
done


#
