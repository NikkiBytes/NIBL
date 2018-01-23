import dicom
import dicom.dataset
import hashlib
import logging
import requests
import BeautifulSoup
import re
import fnmatch
logging.basicConfig(level=logging.INFO)

class Downloader(object):
    log = logging.getLogger(__name__)
    session = None
    queryurl = None
    def __init__(self, username, password, remotehost="https://152.2.112.193", remoteport="3333"):
        self.session = requests.Session()
        payload = {'login':'Login', 'username':username, password:'',
            'sha1':hashlib.sha1(password + username).hexdigest()}
        resp = self.session.post(remotehost+":"+str(remoteport)+"/main", data=payload)
        if(resp.status_code != 200):
            raise IOError('bad username or password')
        self.queryurl = remotehost + ":" + str(remoteport)

    def downloadDicomsByPatientID(self, patient_id):
	self.log.info("THIS IS THE PATIENT ID "+str(patient_id))
	name=patient_id.split()
	self.log.info("THIS IS THE NAME "+str(name[0]))
        resp = self.session.get(self.queryurl + '/studyList?searchID={}'.format(patient_id))
	self.log.info("request url is {}".format(resp.url))
        ph = BeautifulSoup.BeautifulSoup(resp.content)
	#this is good separation
	#find all script tags in the html body
        links = ph.body.findAll('script')
	regex = 'zip_link=".*?zip.*?"'
	pattern=re.compile(regex)
	
	full_script="".join([str(item) for item in links])
	self.log.info("THIS IS LINKS " + str(full_script))
	self.log.info("Regex to match is " + str(regex))
	match = pattern.search(str(full_script))
	self.log.info("Search output is " + str(match))
#        links = ph.body.findAll('script', text=re.compile("zip_link=\"*\";"))
#        links = ph.body.find('img', attrs={'src':'images/download.png'}).parent
#        download_link = [item for item in links.attrs if type(item) is tuple and item[0] == 'href']
	#download_link = full_script[match.start():match.end()].split('zip_link=')[2].split(';')[0].strip("\"")
	download_link = full_script[(match.start()+9):match.end()].strip("\"")
	self.log.info("Download link is " + download_link)

        self.log.debug(download_link)

        resp = self.session.get(self.queryurl+'/'+download_link, stream=True)
        local_filename = download_link.split('?')[0]
        self.log.debug('writing to file ' + local_filename)
        with open(local_filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        self.log.debug(local_filename)
        return local_filename
