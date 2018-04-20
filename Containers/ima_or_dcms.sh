#/bin/bash


cd /projects/niblab/bids_projects/Data/Eric_Data/wave1/dicoms
folders=(*)
for f in ${folders[@]};
do
cd $f
shopt -s nullglob
if [[ -n $(echo *dcm) ]]
then
ima_files=true
echo "IMA files \t $f"
else
ima_files=false
fi
if [[ ima_files = true]]
echo "HEYYYYY"
cd /projects/niblab/bids_projects/Data/Eric_Data/wave1/dicoms
mv $f /projects/niblab/bids_projects/Data/Eric_Data/wave1/ima_files
else
cd /projects/niblab/bids_projects/Data/Eric_Data/wave1/dicoms
fi
done
