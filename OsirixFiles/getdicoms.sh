#!/bin/bash

while IFS=" " read -r col1 col2
do
    echo "RUNNING SETUP SUBJECTS..........................."
    python setup_subjects.py --getdata --keepdata --osirix_username nibl --osirix_password PASSWORD --osirix_subjName $col1 --studyname BRO_data -s "$col1 $col2" -o
    echo "COMPLETED SUBJECT GRAB --------> MOVING TO BRO DATA...................."
    cd BRO_data
    echo "MOVING TO HPC..........................."
    sshpass -p PASSWORD scp -r -p . nbytes@ht3.renci.org:/projects/niblab/bids_projects/Data/BRO_data
    echo "DIRECTORY BEFORE............................"
    ls /$col1/raw
    ls
    echo "WE ARE NOW REMOVING THE FOLDER......................"
    rm -rf bro* 
    rm -rf BRO*
    echo "DIRECTORY AFTER............................."
    ls
    echo "RETURNING TO MAIN DIRECTORY....................."
    cd /home/mint/Documents/NIBL/OsirixScrape
    echo "DIRECTORY BEFORE............................"
    ls
    echo "WE ARE NOW REMOVING THE ZIP FOLDER......................"
    rm -rf *.zip
    echo "DIRECTORY AFTER............................."
    ls
done < BRO_subs.txt
echo "............................................................................COMPLETED"

