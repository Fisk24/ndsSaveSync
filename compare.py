from datetime import datetime
import time
import os

def ftpToDatetime(ftpTime):
    ### Depricated: Server timestamps may soon be irrelivent ###
    # Convert ftp MDMT timestamp into a datetime objects
    return datetime.strptime(ftpTime, '%Y%m%d%H%M%S')

def generateRefrenceTimestamp():
    refTime =  datetime.now()
    with open('reference.time', 'w') as date:
        date.write(str(refTime))

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
