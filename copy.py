import os
import shutil
import zipfile
import fnmatch
import uuid

class Kit:
    def __init__(self, name, filename):
        self.embellishments = []
        self.papers = []
        self.name = name
        self.filename = filename

def main():
    kits = findAll(".")
    for kit in kits:
        print("* ", kit, " -> ", kits[kit])
    print()
    print()
    print("Starting extraction:")
    print("------------------------------------------")
    extractKits(kits)

def findAll(dir):
    print()
    print("All zip files:")
    print("---------------------------")

    kits = {}
    files = os.listdir(".")
    for file in files:
        if file.endswith(".zip"):
            kits[file] = getType(file)
    return kits

def getType(file):
    if "-pp" in file:
        return "paper"
    if "-ap" in file:
        return "alpha"
    if "-ep" in file:
        return "embellishment"

    options = {1: "embellishment", 2: "alpha", 3: "paper", 4:"other"}
    #DEBUG:
    return options[1];
    goodInput = False
    while not goodInput:
        print()
        print("File: ", file)
        print(" 1) Embellishment")
        print(" 2) Alpha")
        print(" 3) Paper")
        print(" 4) Other")
        action = input("Please Enter the Number (default = 1):")
        if action is "":
            return options[1];
        if action.isdigit():
            actionNum = int(action)
            if actionNum > 0 and actionNum < len(options)+1:
                return options[actionNum]


def extractKits(kits):
    tmpDir = "./tmp";
    kitNames = {}
    x = 0
    for kit in kits:
    # kit = next(iter(kits.keys()))
        x = x + 1
        print()
        print()
        print()
        print("Extracting: ", kit, " ( ", x, " of ", len(kits), ")")
        kitStr = kit.rsplit("-", 1)[0]
        print("Kit Name: ", kitStr)
        if kitStr in kitNames:
            name = input("Please Enter Kit Name (default = "+kitNames[kitStr]+"): ")
            name = name or kitNames[kitStr]
        else:
            name = input("Please Enter Kit Name: ")
            kitNames[kitStr] =name

        if os.path.exists(tmpDir):
            shutil.rmtree(tmpDir)
        else:
            os.makedirs(tmpDir)

        if not os.path.exists("./" + name):
            os.makedirs("./" + name)
        kitzip = zipfile.ZipFile("./" + kit)
        kitzip.extractall(tmpDir)
        images = copyExtractedFiles("./" + name +"/")
        createManifest(kit, name, images, kits[kit])

def copyExtractedFiles(dest):
    matches = []
    filenames = [".png", ".jpg"]
    for rootpath, subdirs, files in os.walk("./tmp"):
        for filename in files:
            if os.path.splitext(filename)[1].lower() in filenames:
                # print(os.path.join(rootpath, filename).replace('\\','/'))
                shutil.move(os.path.join(rootpath, filename).replace('\\','/'), dest+filename)
                matches.append(dest + filename)
    return matches


def createManifest(kit, name, images, type):
    manifest = []
    manifest.append('<Manifest vendorid="0" vendorpackageid="0" maintaincopyright="True" dpi="300">')
    manifest.append('<Groups />')
    manifest.append('<Entries>')
    for image in images:
        manifest.append('<Image ID="'+str(uuid.uuid4())+'" Name="'+image+'" Group="Embellishment" />')
    manifest.append('</Entries>')
    manifest.append('</Manifest>')

    with open('./'+name+'/package.manifestx', 'w') as f:
        for line in manifest:
            f.write(line + os.linesep)


if __name__ == "__main__":
    main()
