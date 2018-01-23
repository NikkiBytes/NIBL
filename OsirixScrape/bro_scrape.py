import dryscrape
import subprocess
from bs4 import BeautifulSoup


print "I AM STARTING PROGRAM.....GETTING URLS......................"
url_base = 'http://152.2.112.193:3333/main'
url_target = "http://152.2.112.193:3333/studyList?browse=all"


print "STARTING DRYSCRAPE........"

dryscrape.start_xvfb()

session = dryscrape.Session()
session.visit(url_base)

print "LOGGING IN....................................."

x = session.at_xpath('//*[@name="username"]')
x.set("nibl")
x = session.at_xpath('//*[@name="password"]')
x.set("eatthisnotthat")
login = session.at_xpath('//*[@name="login"]')
login.click()

session.visit(url_target)
page = session.body()
soup = BeautifulSoup(page, 'lxml')

ids = []
patient_tag_ids = soup.find_all('span', class_="study-list-patient-id")

print "OPENING FILE....................................."

file = open("BRO_subs.txt", "w")


for id in patient_tag_ids:
    subject= id.text.split(" ")[0]
    if "BRO" in subject:
        ids.append(subject)
        file.write(str(subject) + "\n")
        print "WROTE TO FILE...........SUBJECT: " + str(subject)

    elif "bro" in subject:
        ids.append(subject)
        file.write(str(subject) + "\n")
        print "WROTE TO FILE...........SUBJECT: " + str(subject)

	else:
		print "PASSING.............................."






file.close()
