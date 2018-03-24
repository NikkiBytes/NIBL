import dryscrape
import subprocess
from bs4 import BeautifulSoup

url_base = 'http://152.2.112.193:3333/main'
url_target = "http://152.2.112.193:3333/studyList?browse=all"

dryscrape.start_xvfb()

session = dryscrape.Session()
session.visit(url_base)

x = session.at_xpath('//*[@name="username"]')
#put username in here
x.set("")
x = session.at_xpath('//*[@name="password"]')
#put password in here
x.set("")
login = session.at_xpath('//*[@name="login"]')
login.click()

session.visit(url_target)
page = session.body()
soup = BeautifulSoup(page, 'lxml')

bf_ids = []
patient_tag_ids = soup.find_all('span', class_="study-list-patient-id")


for id in patient_tag_ids:
    if "BF" in id.text:
        bf_ids.append(id.text)


file = open("BF_subjectIDS.txt", "w")

for id in bf_ids:
    print(id)
    id_out = id.split(' ')[0]
    file.write(id + "," + id_out + "\n")



   # bashCommand = 'python setup_subjects.py --getdata --keepdata --osirix_username nibl --osirix_password eatthisnotthat --osirix_subjName %s --studyname SugarMama -s %s -o ' %(id, id_out)
    #print(bashCommand)
    #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

file.close()
