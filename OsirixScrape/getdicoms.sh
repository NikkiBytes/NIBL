#!/bin/bash

while read -r col1
do

    python setup_subjects.py --getdata --keepdata --osirix_username nibl --osirix_password eatthisnotthat --osirix_subjName "$col1" --studyname BRO_data -s "$col1" -o
    echo "COMPLETED SUBJECT GRAB --------> MOVING TO BRO DATA...................."
    cd BRO_data
    echo "RUNNING SETUP SUBJECTS..........................."
    sshpass -p 'sweetbbcs' scp -r -p $col1 nbytes@ht3.renci.org:/projects/niblab/bids_projects/Data/BRO_data
    echo "DIRECTORY BEFORE............................"
    ls
    echo "WE ARE NOW REMOVING THE FOLDER......................"
    rm -rf $col1
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

