import os
import misc
import kit

def Header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print()
    print("Select the folder with the downloaded files")
    print("--------------------------------------------------------------------")
    print()

def HeaderKits():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print()
    print("Find all of the zip in the choosen folder")
    print("--------------------------------------------------------------------")
    print()

def SelectFolder():
    Header()
    homedir = os.path.expanduser("~")
    downloadDir = os.path.join(homedir, "Downloads")

    if os.path.isdir(downloadDir):
        while True:
            print("Your Download folder is '" + downloadDir + "'")
            inDownloadDir = misc.ConfirmInput("Are the scrapbook zip files in your downloads folder? ", True)
            if inDownloadDir:
                return downloadDir
            else:
                return GetCustomDir();

            Header()
            print()
            print(" Error!")
            print(" The input '" + inDownloadDir + "' doesn't seemed to work, please try again")
            print()
            print()

    else:
        return GetCustomDir()

def GetCustomDir():
    while True:
        Header()
        print()
        print("Please enter the path to the folder where your files are at")
        print()
        print("Some Helpful Notes:")
        print(" * Find folder path first in the file explore program")
        print(" * Copy the path to this folder")
        print(" * Try right clicking this windows to paste")
        print(" * If you really stuck, use Google")
        print()

        folder = input("Path: ")
        if folder is not "" and os.path.isdir(folder):
            return folder
        else:
            print()
            print("That doesn't seem to be a folder, please try again")
            print()

def FindAllKits(dir):
    HeaderKits()

    kitFiles = []
    files = os.listdir(dir)
    for file in files:
        if file.lower().endswith(".zip"):
            kitFiles.append(file)
    return kitFiles
