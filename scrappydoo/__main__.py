import sys
import os
import argparse
import misc
import folderParser
import kit
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

    print("Found:")
    print(kitFiles)
    input()

    kits = kit.ProcessKits(kitFiles)
    for k in kits:
        print(kits[k])
    print()
    print()
    print()
    print("Done!")

if __name__ == "__main__":
    main(sys.argv[1:])
