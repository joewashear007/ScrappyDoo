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

    #pre kit processing screen
    misc.SetHeader("Quick Message")
    print("We are going all of the Art Kits in: ", folder )
    print("For each zile file we find:")
    print(" * You can enter the name of the Art Kit it is part of")
    print(" * What type of elements it holds")
    print(" * Skip any file that is not part of an Art Kit")
    print(" * If an option has '(Default)', it can be choosen with just pressing 'Enter'")
    print()
    print("Lets Get Started! ")
    misc.Pause()

    kits = kitutil.ProcessKits(kitFiles)
    kitutil.ExtractKits(kits, folder)

    # Post processing - Move Files
    kitutil.MoveKitFolders(kits, folder)

    # Post processing - Delete zips
    misc.SetHeader("Kit Post Processing")
    print("Would you like me to delete the zip files that were turn into kits?")
    print("They shouldn't be needed any more if everything install correctly into Creative Memories")
    print()
    print("WARNING: This can NOT be undone!")
    print()
    shouldDelete = misc.ConfirmInput("Should I delete the zip files that you ?")
    if shouldDelete:
        kitutil.DeleteKitFiles(kits, folder)


    # Closing msg
    misc.SetHeader("Good Bye!")
    print("Everything is complete!")
    print("Thanks for using ScrappyDoo and have a nice day!")
    print()
    misc.Pause()

if __name__ == "__main__":
    main(sys.argv[1:])
