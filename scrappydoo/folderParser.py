import os

def Header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print()
    print("Select the folder with the downloaded files")
    print("--------------------------------------------------------------------")
    print()

def SelectFolder():
    Header()
    homedir = os.path.expanduser("~")
    downloadDir = os.path.join(homedir, "Downloads")

    if os.path.isdir(downloadDir):
        while True:
            print("The scrapbook zip files in your downloads folder? ")
            print("That folder is '" + downloadDir + "'")
            print(" 1) Yes")
            print(" 2) No")
            inDownloadDirStr = input("Please Select: ")
            if inDownloadDirStr.isdigit():
                inDownloadDir = int(inDownloadDirStr)
                if inDownloadDir == 1 :
                    return downloadDir
                if inDownloadDir == 2:
                    return GetCustomDir();

            Header()
            print()
            print(" Error!")
            print(" The input '" + inDownloadDirStr + "' doesn't seemed to work, please try again")
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
