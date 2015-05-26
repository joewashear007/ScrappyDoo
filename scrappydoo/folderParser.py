import os
import misc
import kit

def SelectFolder():
    misc.SetHeader("Select the folder with the downloaded files")
    homedir = os.path.expanduser("~")
    downloadDir = os.path.join(homedir, "Downloads")

    if os.path.isdir(downloadDir):
        while True:
            print("Your Download folder is '" + downloadDir + "'")
            inDownloadDir = misc.ConfirmInput("Are the scrapbook zip files in your downloads folder? ", True)
            if inDownloadDir:
                return downloadDir
            else:
                return misc.GetDir("Please enter the path to the folder where your files are at")
            misc.SetHeader("Select the folder with the downloaded files")
            print()
            print(" Error!")
            print(" The input '" + inDownloadDir + "' doesn't seemed to work, please try again")
            print()
            print()
    else:
        return misc.GetDir("Please enter the path to the folder where your files are at")

def FindAllKits(dir):
    misc.SetHeader("Finding all of the zip in: " + dir)

    kitFiles = []
    files = os.listdir(dir)
    for file in files:
        if file.lower().endswith(".zip"):
            kitFiles.append(file)
    return kitFiles
