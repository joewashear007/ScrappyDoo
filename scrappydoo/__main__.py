import sys
import os
import argparse
import misc
import folderParser
import kitutil
import pprint

def main(args):
    parser = argparse.ArgumentParser(description='ScrappyDoo')
    # parser.add_argument('path', nargs='?', type="string")
    # parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),default=sys.stdout)
    parser.parse_args();
    args = parser.parse_args()
    misc.Welcome()
    folder = folderParser.SelectFolder()
    kitFiles = folderParser.FindAllKits(folder)
    kits = kitutil.ProcessKits(kitFiles)
    kitutil.ExtractKits(kits, folder)
    print()
    print()
    print()
    print("Done!")

if __name__ == "__main__":
    main(sys.argv[1:])
