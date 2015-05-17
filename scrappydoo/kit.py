import os

class Kit:
    def __init__(self, name):
        self.name = name
        self.paperFiles = []
        self.embellishmentFiles = []
        self.alphaFiles = []


class KitZip:
    def __init__(self, filename):
        self.type = ""
        self.name = ""
        self.filename = filename
        self.GetInfo()

    def GetInfo(self):
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
            print("Found File: ", file)
            print(" 1) Embellishment")
            print(" 2) Alpha")
            print(" 3) Paper")
            print(" 4) Other")
            action = input("Please0x Enter the Number (default = 1):")
            if action is "":
                return options[1];
            if action.isdigit():
                actionNum = int(action)
                if actionNum > 0 and actionNum < len(options)+1:
                    return options[actionNum]

def Header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print()
    print("Sort the kit files")
    print("--------------------------------------------------------------------")
    print()

def ProcessKits(kitFiles):
    options = {1: "embellishment", 2: "alpha", 3: "paper", 4:"other"}

    for kitFile in kitFiles:
        Header()
        while True:
            print()
            print("Found File: ", kitFile)
            print()
            print("Please choose what this kit is")
            print(" 1) Embellishment")
            print(" 2) Alpha")
            print(" 3) Paper")
            print(" 4) Other")
            print(" 5) Skip, this is not a kit!")
            print()
            action = input("Please Select (default = 1):")
            if action is "":
                return options[1];
            if action.isdigit():
                actionNum = int(action)
                if actionNum > 0 and actionNum < len(options)+1:
                    return options[actionNum]

def GetKitName(file):
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
