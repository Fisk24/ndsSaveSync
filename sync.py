from ftplib import FTP
import os
import re
import sys
import compare
import convert
import argparse

HOST = "10.71.8.43"
PORT = 5000

REMOTE_DIR = "/roms/nds"
LOCAL_DIR = "raw_data/"
DESMUME_SAVES = "Battery/"

def setIPandPort(args):
    global HOST
    global PORT

    connStr = args.ip_and_port.split(":")

    HOST = connStr[0]
    PORT = int(connStr[1])

def getRemoteDir(ftp, _dir=""):
    file_list  = []
    file_names = [] # [{name: NAME, mtime: TIMESTAMP}]
    ftp.retrlines("LIST "+_dir, file_list.append)
    for file in file_list:
        #print(file)
        filename = re.sub(' +', ' ', file) # Clean out extra spaces such that the output of LIST can be reliabley parsed
        filename = filename.split(" ")[8:] # Split by spaces, then splice out everything except the file name
        filename = " ".join(filename)      # Rejoin into string, which by now should represent only the file name

        #timestamp = ftp.sendcmd("MDTM "+filename).split(" ")[1]
        #timestamp = compare.ftpToDatetime(timestamp)

        file_names.append(filename)

    return file_names

def retriveSaveData(ftp, remoteDir):
    os.makedirs(LOCAL_DIR, exist_ok=True)
    for _file in remoteDir:
        if '.sav' in _file:
            print("Downloading", _file)
            with open(LOCAL_DIR+_file, 'wb') as save:
                ftp.retrbinary("RETR "+_file, save.write)

def fetch3dsSaves():
    print(">>> Fetching remote save data")
    with FTP() as ftp:
        ftp.connect(HOST, PORT)
        ftp.cwd(REMOTE_DIR)
        remoteDir = getRemoteDir(ftp)
        retriveSaveData(ftp, remoteDir)

def launchDesmume():
    if sys.platform == 'win32':
        os.system("DeSmuME_0.9.11_x64.exe")
    elif sys.platform == 'linux':
        os.system("desmume")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('ip_and_port')
    args = parser.parse_args()
    setIPandPort(args)

    #### DOWNLOAD MODE ####

    #### THIS MODE SHOULD FAIL IF refernce.time EXISTS ####

    fetch3dsSaves()
    convert.batchConvertToDsv(LOCAL_DIR, DESMUME_SAVES)
    compare.generateRefrenceTimestamp()
    compare.generateRefrenceMD5(DESMUME_SAVES)
    launchDesmume()


    sys.exit()
        # Real usecase will compare against the converted DSV as those are what will have changed

        #compare.getChangeList(LOCAL_DIR)


    #### UPLOAD MODE ####


    # Make the command-lind switches for this mode
    # MAKE A BACKUP OF 3DS' FILES BEFORE EVEN ATTEMPTING TO CREATE THIS MODE


    #
