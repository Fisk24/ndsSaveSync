import mmap
import sys
import os
import argparse

desmumeFooterIndex = -122
desmumeFooterData = b'|<--Snip above here to create a raw sav by excluding this DeSmuME savedata footer:\x00\x00\x08\x00\x00\x00\x08\x00\x06\x00\x00\x00\x03\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00|-DESMUME SAVE-|'

def writeBinary(saveData, saveFile):
    with open(saveFile, 'wb') as sf:
        sf.write(saveData)

def dsv_to_sav(saveFile, outputDir = ""):
    print("Converting DeSmuMe save data to RAW save data...", end="")
    basename = saveFile.split(".dsv")[0].split("/")[-1] # Remove the dsv extention from the file name so we dont have to do it later
    with open(saveFile, "r+b") as f:                    # Open the dsv file
        with mmap.mmap(f.fileno(), 0) as mm:            # Load the dsv into a memory map so that the file can be edited on the byte level
            rawsavemap = mm[:desmumeFooterIndex]        # Isolate the save data from the demume footer using list splicing then store it in a variable for later
    writeBinary(rawsavemap, outputDir+basename+".sav")  # Write the buffer with an sav extention and the conversion process is complete
    print("done")

def sav_to_dsv(saveFile, outputDir = ""):
    print("Converting RAW save data to DeSmuMe save data...", end="")
    baseName = saveFile.split(".sav")[0].split("/")[-1] # Remove the sav extention from the file name so we dont have to do it later
    with open(saveFile, "r+b") as f:                    # Open the sav file in read binary mode
        rawSaveData = f.read()                          # Read the bytes into a variable for later use
        dsvSaveData = rawSaveData + desmumeFooterData   # Combine the raw save data with desmume footer data
    writeBinary(dsvSaveData, outputDir+baseName+".dsv") # Write the new desmume save data to a file with the dsv extention and the conversion process is complete
    print("done")

def batchConvertToDsv(inDir, outDir = ""):
    print(">>> Converting save data...")
    for f in os.listdir(inDir):
        if f.split(".")[-1].lower() == 'sav':
            sav_to_dsv(inDir+f, outDir)

def batchConvertToSav(inDir, outDir):
    print(">>> Converting desmume save data")
    for f in os.listdir(inDir):
        if f.split(".")[-1].lower() == 'dsv':
            dsv_to_sav(inDir+f, outDir)

def main():
    parser = argparse.ArgumentParser(description="Convert NDS save files from dsv to sav and vice versa.")
    sub_parsers = parser.add_subparsers(dest="subparser_name")

    dts_parser = sub_parsers.add_parser('dts')
    dts_parser.add_argument('dsv_save_file', help="DSV file to target for conversion")

    std_parser = sub_parsers.add_parser('std')
    std_parser.add_argument('sav_save_file', help="SAV file to target for conversion")

    args = parser.parse_args()

    #print(args)
    if args.subparser_name == "dts":
        dsv_to_sav(args.dsv_save_file)
    if args.subparser_name == "std":
        sav_to_dsv(args.sav_save_file)

if __name__ == "__main__":
    main()
