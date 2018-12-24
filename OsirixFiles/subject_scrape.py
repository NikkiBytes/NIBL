import dryscrape
import subprocess
from bs4 import BeautifulSoup

print "GETTING URL......"
url_base = 'http://152.2.112.193:3333/main'
url_target = "http://152.2.112.193:3333/studyList?browse=all"

print "STARTING DRYSCRAPE......"

dryscrape.start_xvfb()

session = dryscrape.Session()
session.visit(url_base)

print "GETTING PASSWORD AND USER......"

x = session.at_xpath('//*[@name="username"]')
x.set("nibl")
x = session.at_xpath('//*[@name="password"]')
x.set("eatthisnotthat")
login = session.at_xpath('//*[@name="login"]')
login.click()
print "I AM VISITING TARGET URL NOW"
session.visit(url_target)
page = session.body()
soup = BeautifulSoup(page, 'lxml')

ids = []
patient_tag_ids = soup.find_all('span', class_="study-list-patient-id")



    
#print patient_tag_ids
for id in patient_tag_ids:
    if "BRO" in id.text:
        print "RUNNING SUBPROCESS NOW........"
        temp_sub= id.text
        subject = temp_sub.split(" ")[0]
        print "WORKING ON SUBJECT......" + str(subject)
        #ids.append(id.text)
        #print id.text
        command=["python setup_subjects.py --getdata --keepdata --osirix_username nibl --osirix_password  eatthisnotthat --osirix_subjName " + subject + "  --studyname BRODATA -s " + subject + " -o " ]
        subprocess.Popen(command, shell=True)
        command2 = [ "sshpass -p sweetbbcs scp -r -p /BRODATA/" + str(subject) + " nikkibytes@ht1.renci.org:/projects/niblab/bids_projects" ]
        subprocess.Popen(command2, shell=True)
        #command3=["rm -rf *.zip; cd BRODATA; ls; rm -rf " + str(subject) + " cd /home/mint/Documents/Osirix_Scraper"]
        #subprocess.Popen(command3, shell=True)
        
        print "COMPLETED"
        
#for id in patient_tag_ids:
    if "bro" in id.text:
        print "RUNNING SUBPROCESS NOW........"
        temp_sub= id.text
        subject = temp_sub.split(" ")[0]
        print "WORKING ON SUBJECT......" + str(subject)
        #ids.append(id.text)
        #print id.text
        command=["python setup_subjects.py --getdata --keepdata --osirix_username nibl --osirix_password  eatthisnotthat --osirix_subjName " + subject + "  --studyname BRODATA -s " + subject + " -o " ]
        subprocess.Popen(command, shell=True)
        command2 = [ "sshpass -p sweetbbcs scp -r -p /BRODATA/" + str(subject) + " nikkibytes@ht1.renci.org:/projects/niblab/bids_projects" ]
        subprocess.Popen(command2, shell=True)
        #command3=["rm-rf *.zip; cd BRODATA; ls; rm -rf " + str(subject) + " cd /home/mint/Documents/Osirix_Scraper"]
        #subprocess.Popen(command3, shell=True)
        print "COMPLETED"
        
#print(ids)
#file = open("BF_subjectIDS.txt", "w")


#subject = ids[0].split(" ")[0]
#print subject
#subprocess.Popen(['python', 'setup_subjects.py', '--getdata', '--keepdata', '--osirix_username', 'nibl', '--osirix_password', 'eatthisnotthat', '--osirix_subjName',  subject, '--studyname', 'BRODATA' '-s', subject, '-o', 'Bro_data' ])
#command=["python setup_subjects.py --getdata --keepdata --osirix_username nibl --osirix_password  eatthisnotthat --osirix_subjName " + subject + "  --studyname BRODATA -s " + subject + " -o " ]
#subprocess.Popen(command, shell=True)





'''
for id in ids:
    print(id)
    subject = id.split(' ')[0]
#    file.write(id + "," + id_out + "\n")
    print "I am hereC"



    subprocess.Popen(['python', 'setup_subjects.py', '--getdata', '--keepdata', '--osirix_username', 'nibl', '--osirix_password', 'eatthisnotthat', '--osirix_subjName',  _subject, '--studyname', '', '-s', _subject, '-o'])

#file.close()
'''