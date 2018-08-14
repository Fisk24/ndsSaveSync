from ftplib import FTP
import os
import re
import sys
import compare
import convert
import argparse

HOST = "10.71.8.43"
PORT = 5000
TIMEOUT = 5

REMOTE_DIR = "/roms/nds"
LOCAL_DIR = "raw_data/"
DESMUME_SAVES = "Battery/"

ONLINE_MODE = True

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
    global ONLINE_MODE
    try:
        print(">>> Fetching remote save data")
        with FTP() as ftp:
            ftp.connect(HOST, PORT, TIMEOUT)
            ftp.cwd(REMOTE_DIR)
            remoteDir = getRemoteDir(ftp)
            retriveSaveData(ftp, remoteDir)
    except ConnectionRefusedError as e:
        print("Connection was refused, or the target 3ds system does not have an FTP server running.")
        ONLINE_MODE = False

def launchDesmume():
    if sys.platform == 'win32':
        os.system("DeSmuME_0.9.11_x64.exe")
    elif sys.platform == 'linux':
        os.system("desmume")

def reupload3dsSaves():
    try:
        print(">>> Reuploading saves files")
        change_list = compare.getChangeList(DESMUME_SAVES, LOCAL_DIR)
        with FTP() as ftp:
            ftp.connect(HOST, PORT, TIMEOUT)
            ftp.cwd(REMOTE_DIR)
            for i in change_list:
                file_name = i.split('.')[0]+'.sav'
                print("Uploading", file_name)
                with open(LOCAL_DIR+file_name, 'rb') as outFile:
                    ftp.storbinary("STOR "+file_name, outFile)
    except ConnectionRefusedError as e:
        print("Could not upload the modified save data...")
        print("Make sure the 3ds ftp server is online and run the script again...")
        sys.exit()

def createUsageToken():
    with open("usage.token", 'wb') as usage:
        usage.write(b'x00')

def destroyUsageToken():
    os.remove('usage.token')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('ip_and_port')
    args = parser.parse_args()
    setIPandPort(args)

    # Add a commandline switch to allow the script to work offline using existing saves
    # The script should always upload unrecognized saved data (Save data that was not listed in the 3ds's directory)

    if not os.path.isfile('usage.token'):
        createUsageToken()
        fetch3dsSaves()
        if ONLINE_MODE == True:
            convert.batchConvertToDsv(LOCAL_DIR, DESMUME_SAVES)
            compare.generateRefrenceTimestamp()
            compare.generateRefrenceMD5(DESMUME_SAVES, LOCAL_DIR)
    launchDesmume()
    compare.printMD5ComparisonTable()
    convert.batchConvertToSav(DESMUME_SAVES, LOCAL_DIR)
    reupload3dsSaves()
    destroyUsageToken()

    sys.exit()
