from datetime import datetime
import time
import os
import hashlib

def ftpToDatetime(ftpTime):
    ### Depricated: Server timestamps may soon be irrelivent ###
    # Convert ftp MDMT timestamp into a datetime objects
    return datetime.strptime(ftpTime, '%Y%m%d%H%M%S')

def generateRefrenceTimestamp():
    print(">>> Generated reference time file...")
    refTime =  datetime.now()
    print(refTime)
    with open('reference.time', 'w') as date:
        date.write(str(refTime))

def generateRefrenceMD5(outDir):
    print(">>> Generating refrence MD5's")
    print("But i can't write them yet :C")
    for f in os.listdir(outDir):
        if ".dsv" in f:
            hash_md5 = hashlib.md5()
            with open(outDir+f, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            print(hash_md5.hexdigest())

def getRefrenceTimestamp():
    with open('reference.time', 'r') as date:
        return datetime.strptime(date.read(), '%Y-%m-%d %H:%M:%S.%f')

def getChangeList(changeDir):
    refTime = getRefrenceTimestamp()
    for f in os.listdir(changeDir):
        modTime = datetime.fromtimestamp(os.path.getmtime(changeDir+f))
        timeDelta = refTime - modTime
        print(timeDelta.total_seconds())


def main():
    print(datetime.datetime.utcfromtimestamp(\
        os.path.getmtime("compair.py"))\
        .strftime('%Y%m%d%H%M%S'))

if __name__ == "__main__":
    main()
