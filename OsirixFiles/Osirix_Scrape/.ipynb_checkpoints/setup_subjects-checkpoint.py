#!/usr/bin/env python

import argparse
import os, sys
from datetime import datetime
import dicom

from osirixdownloader import downloader

import random
import string
import zipfile


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# parse_command_line() function parses the input command line


def parse_command_line():
    directory_path = '/home/mint'
    parser = argparse.ArgumentParser(description='setup_subject')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',help='an integer for the accumulator')
    # set up boolean flags


    parser.add_argument('--getdata', dest='getdata', action='store_true',
                        default=False, help='get data from XNAT')
    parser.add_argument('--keepdata', dest='keepdata', action='store_true',
                        default=False, help='keep DICOMs after conversion')
    parser.add_argument('--dcm2nii', dest='dcm2nii', action='store_true',
                        default=False, help='perform dicom conversion')
    parser.add_argument('-o', dest='overwrite', action='store_true',
                        default=False, help='overwrite existing files')
    parser.add_argument('-t', dest='testmode', action='store_true',
                        default=False, help='run in test mode (do not execute commands)')
    parser.add_argument('--motcorr', dest='motcorr', action='store_true',
                        default=False, help='run motion correction')
    parser.add_argument('--betfunc', dest='betfunc', action='store_true',
                        default=False, help='run BET on func data')
    parser.add_argument('--qa', dest='qa', action='store_true',
                        default=False, help='run QA on func data')
    parser.add_argument('--fm', dest='fm', action='store_true',
                        default=False, help='process fieldmap')
    parser.add_argument('--dtiqa', dest='dtiqa', action='store_true',
                        default=False, help='run QA on DTI data')
    parser.add_argument('--topup', dest='topup', action='store_true',
                        default=False, help='run topup on DTI data')
    parser.add_argument('--melodic', dest='melodic', action='store_true',
                        default=False, help='run melodic on func data')
    parser.add_argument('--unzip', dest='unzip', action='store_true',
                        default=False, help='unzip data file')
    parser.add_argument('--fsrecon', dest='fsrecon', action='store_true',
                        default=False, help='run freesurfer autorecon1')
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='give verbose output')
    parser.add_argument('--bet-inplane', dest='bet_inplane', action='store_true',
                        default=False, help='run bet on inplane')
    parser.add_argument('--all', dest='doall', action='store_true',
                        default=False, help='run all steps')

    # set up flags with arguments

    #    parser.add_argument('--xnat_server', dest='xnat_server',
    #        help='URL for xnat server',default="https://xnat.irc.utexas.edu/xnat-irc")
    parser.add_argument('--osirix_username', dest='osirix_username',
                        help='user name for osirix server', default='')
    parser.add_argument('--osirix_password', dest='osirix_password',
                        help='password for osirix server', default='')
    parser.add_argument('--osirix_subjName', dest='osirix_subjName',
                        help='the name of the subject as it appears in the patient ID in osirix')
    parser.add_argument('-f', dest='filename',
                        help='path to zipped data file')
    parser.add_argument('--studyname', dest='studyname',
                        help='name of study', required=True)
    parser.add_argument('-b', dest='basedir',
                        help='base directory for data file', default=directory_path)
    parser.add_argument('-s', '--subcode', dest='subcode',
                        help='subject code', required=True)
    parser.add_argument('--subdir', dest='subdir',
                        help='subject dir (defaults to subject code)', default='')
    parser.add_argument('--mcflirt-args', dest='mcflirt_args',
                        help='arguments for mcflirt', default='-plots -sinc_final')
    #    parser.add_argument('--xnat-project', dest='xnat_project',
    #        help='project in XNAT',default='poldrack')
    parser.add_argument('--mricrondir', dest='mricrondir',
                        help='directory for mricron', default='')
    parser.add_argument('--fs-subdir', dest='fs_subdir',
                        help='subject directory for freesurfer', default=directory_path)
    parser.add_argument('--bet-highres', dest='bet_highres', action='store_true', default=False,
                        help='run bet on highres image')

    args = parser.parse_args()
    arglist = {}
    for a in args._get_kwargs():
        arglist[a[0]] = a[1]

    return arglist
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## setup_dir() takes the arguments and sets up a directory

def setup_dir(args):
    print("I am in setup_dir")
    # basedir for data
    studyname = args['studyname']
    subcode = args['subcode']
    print( "..... " + studyname)
    print("..... " + subcode)
    if args['verbose']:
        print(subcode)

    print(args['basedir'])
    studydir = os.path.join(args['basedir'], studyname)
    if not os.path.exists(studydir):
        print('ERROR: study dir %s does not exist!' % studydir)
        sys.exit()
        # subcode=sys.argv[1]

    #                destination = str(destination).replace(' ', '_')
    subdir = os.path.join(studydir, args['subdir'])


    if not os.path.exists(subdir):
        os.makedirs(subdir)
    else:
        print('subdir %s already exists' % subdir)
        if args['overwrite'] == False:
            sys.exit()
        else:
            print('overwriting...')

    ### HERE IS WHERE WE ARE MAKING DIRECTORIES
    ### Do we need them?
    subdirs = 'raw'
    subdir_names = {}


    subdir_names[subdirs] = os.path.join(subdir, subdirs)
    if not os.path.exists(subdir_names[subdirs]):
        os.makedirs(subdir_names[subdirs])

    return subdir, subdir_names

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



# setup_outfiles() sets up output files


def setup_outfiles():
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    outfile = {}
    outfile['main'] = os.path.join(subdir, 'logs/cmd_' + timestamp + '.log')
    outfile['dcm2nii'] = os.path.join(subdir, 'logs/dcm2nii_cmd_' + timestamp + '.log')
    outfile['unzip'] = os.path.join(subdir, 'logs/unzip_' + timestamp + '.log')

    #log_message("#command file automatically generated by setup_subject.py\n#Started: %s\n\n" % timestamp, outfile['main'])
    return outfile



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# download_from_osirix() is the datagrabber function, activated from the --getdata cmd argument

def download_from_osirix(args, osirix_subjName):
    dl = downloader.Downloader(args['osirix_username'], args['osirix_password'], remotehost="http://152.2.112.193",
                               remoteport="3333")
    #        dl=downloader.Downloader(args['osirix_username'],args['osirix_password'])
    print(args['osirix_subjName'])
    datazip = dl.downloadDicomsByPatientID(args['osirix_subjName'])
    ziphandle = zipfile.ZipFile(datazip)
    if not os.path.exists(os.path.join(subdir, 'raw', args['subcode'])):
        os.makedirs(os.path.join(subdir, 'raw', args['subcode']))
    ziphandle.extractall(os.path.join(subdir, 'raw', args['subcode']))
   # os.unlink(datazip)
    for item in os.listdir(os.path.join(subdir, 'raw', args['subcode'])):
        path, ext = os.path.splitext(item)
        if ext != '.dcm':
            print('continuing')
            continue
        item = os.path.join(subdir, 'raw', args['subcode'], item)
        headers = dicom.read_file(item)
        newitemname = get_xnat_name(headers)
        destination = os.path.join(subdir, 'raw', args['subcode'], str(headers.SeriesNumber))
        #                destination = str(destination).replace(' ', '_')
        if not os.path.exists(destination):
            os.makedirs(destination)
        os.rename(item, os.path.join(destination, newitemname))




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def do_unzipping(args, subdir):

    if not args['filename'] or not os.path.exists(args['filename']):
        print('filename %s not found for unzipping - exiting' % args['filename'])
        sys.exit()
    # cmd='unzip %s -d %s'%(args['filename'],subdir)
    cmd = 'unzip %s ' % (args['filename'])
    print(cmd)
    if not args['testmode']:
        run_logged_cmd(cmd, outfile['unzip'])


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def get_xnat_name(header):
    name = str()
    name += str(header.PatientName) if str(header.PatientName) != '' else 'Subject'
    name += '.'
    try:
        name += str(header.RequestedProcedureDescription) if str(
            header.RequestedProcedureDescription) != '' else 'Procedure'
    except:
        name += 'Procedure'
    name += '.'
    name += str(header.SeriesNumber) if str(header.SeriesNumber) != '' else 'num'
    name += '.'
    name += str(header.InstanceNumber) if str(header.InstanceNumber) != '' else 'inst'
    name += '.'
    name += str(header.StudyDate) if str(header.StudyDate) != '' else 'date'
    name += '.'
    name += str(header.StudyTime).replace('.', '') if str(header.StudyTime) != '' else 'time'
    name += '.'
    name += ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(7))
    name += '.dcm'
    return name

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

args = parse_command_line()

doall_cmds = ['dcm2nii', 'motcorr', 'betfunc', 'qa', 'melodic', 'bet_inplane', 'fsrecon']
if args['doall']:
    for c in doall_cmds:
        args[c] = True
        print("True")






if args['subdir']=='':
    print("hello")
    args['subdir']=args['subcode']
    print("subdir args: " + args['subdir'])


args['fs_subcode']='%s_%s'%(args['studyname'],args['subdir'])
print("fs_subcode args: " + args['fs_subcode'])

print("I am here, processing, and doing the thang!")



subdir, subdir_names = setup_dir(args)

print("I am out of setup_dir")
print("....running setup_outfiles()")
outfile = setup_outfiles()



if args['getdata']:
    download_from_osirix(args, subdir)



if args['unzip']:
    do_unzipping(args, subdir)

print("....finished do_unzipping()")
