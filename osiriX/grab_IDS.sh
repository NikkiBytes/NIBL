#!/bin/bash

# Title: OsiriX Scrape
# Author: Nichollette Acosta
# University of North Carolina at Chapel Hill, Neuropsychology of Ingestive Behavior Labortary


# To pull a specific subject ID, run following:
#  SM1564-1
# python setup_subjects.py --getdata --keepdata --osirix_username nibl --osirix_password eatthisnotthat --osirix_subjName "SM1564-1" --studyname SugarMama -s "SM1564-1" -o

while IFS=',' read -r col1 col2
do

    python setup_subjects.py --getdata --keepdata --osirix_username nibl --osirix_password YOUR_PASSWORD_HERE --osirix_subjName "$col1" --studyname BreakfastClub -s "$col2" -o

done < BF_subjectIDS.txt
