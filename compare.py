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

def generateRefrenceMD5(inDir, outDir):
    ### Create md5 files for the converted saves ###
    print(">>> Generating refrence MD5's")
    for f in os.listdir(inDir):
        if f.split(".")[-1].lower() == 'dsv':
            md5 = getMD5(inDir+f)
            writeMD5(md5, outDir+f+".md5")

def decisionKeepReject(refMD5, refTime, modMD5, modTime):
    md5isDifferent = (refMD5 != modMD5)
    timeDeltaIsSignificant = ((refTime - modTime).total_seconds() < -10)
    return (md5isDifferent and timeDeltaIsSignificant)

def getMD5(inFile):
    hash_md5 = hashlib.md5()
    with open(inFile, "rb") as dsv:
        for chunk in iter(lambda: dsv.read(4096), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

def getReferenceTimestamp():
    with open('reference.time', 'r') as date:
        return datetime.strptime(date.read(), '%Y-%m-%d %H:%M:%S.%f')

def getChangeList(stagDir, refDir):
    # Return a list of files that have changed given the md5 and date modified #
    change_list = []
    for candidate in os.listdir(stagDir):
        if (".dsv" in candidate):
            refMD5 = readMD5(refDir+candidate+'.md5')
            modMD5 = getMD5(stagDir+candidate)
            refTime = getReferenceTimestamp()
            modTime = datetime.fromtimestamp(os.path.getmtime(stagDir+candidate))
            timeDelta = refTime - modTime
            if (decisionKeepReject(refMD5, refTime, modMD5, modTime) == True):
                change_list.append(candidate)
    return change_list

def readMD5(inFile):
    with open(inFile, 'r') as md5:
        return md5.read()

def writeMD5(inString, outFile):
    with open(outFile, "w") as md5:
        hexdigest = inString
        md5.write(hexdigest)
        print(outFile, "-->", hexdigest)

def printMD5ComparisonTable(refDir):
    print(">>> Comparison Table")
    for i in os.listdir(refDir):
        if (".dsv" in i):
            try:
                refMD5 = readMD5('raw_data/'+i+'.md5')
            except FileNotFoundError as e:
                # If the comparison md5 is not found, it is possible that a new save game could have been created locally and would likely need to be uploaded
                print(e, "Skipping comparison...")
                print("--------------------------------------")
                continue

            modMD5 = getMD5(refDir+i)
            refTime = getReferenceTimestamp()
            modTime = datetime.fromtimestamp(os.path.getmtime(refDir+i))
            timeDelta = refTime - modTime

            if (decisionKeepReject(refMD5, refTime, modMD5, modTime) == True):
                decision = "True: Keeping..."
            else:
                decision = "False: Rejecting..."

            print(i)
            print(refMD5, refTime, decision) # Print reference
            print(modMD5, modTime, timeDelta.total_seconds()) # Print current md5 after change

            print("--------------------------------------")

def main():
    print(datetime.datetime.utcfromtimestamp(\
        os.path.getmtime("compair.py"))\
        .strftime('%Y%m%d%H%M%S'))

if __name__ == "__main__":
    main()
