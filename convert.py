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
    basename = saveFile.split(".dsv")[0].split("\\")[-1]
    with open(saveFile, "r+b") as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            rawsavemap = mm[:desmumeFooterIndex] # Store raw save data minus the desmume footer
    writeBinary(rawsavemap, outputDir+basename+".sav")
    print("done")

def sav_to_dsv(saveFile, outputDir = ""):
    print("Converting RAW save data to DeSmuMe save data...", end="")
    baseName = saveFile.split(".sav")[0].split("/")[-1]
    with open(saveFile, "r+b") as f:
        rawSaveData = f.read()
        dsvSaveData = rawSaveData + desmumeFooterData

    writeBinary(dsvSaveData, outputDir+baseName+".dsv")
    print("done")

def batchConvertToDsv(inDir, outDir = ""):
    print(">>> Converting save data...")
    for i in os.listdir(inDir):
        sav_to_dsv(inDir+i, outDir)

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
