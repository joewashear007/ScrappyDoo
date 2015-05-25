import os
import misc

class Kit:
    def __init__(self, name):
        self.name = name
        self.files = {}

    def addFile(self, type, filename):
        if type not in self.files:
            self.files[type] = []
        self.files[type].append(filename)

    def __str__(self):
        kstr = self.name +  "(" + str(len(self.files)) + ")\n"
        for type in self.files:
            for f in self.files[type]:
                kstr += type + ": " + f + "\n"
        return kstr

def Header(num, total):
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print()
    print("Get Kit Information (", num, " of ", total, ")")
    print("--------------------------------------------------------------------")
    print()

def ProcessKits(kitFiles):
    kitsZips = {}
    x = 0
    for file in kitFiles:
        x = x + 1
        Header(x, len(kitFiles))
        print("Current File: ", file)
        print("If the file is not a kit or you like like to skip it, please enter '#skip' for the name")
        print()
        kitNameInfo = GetKitName(file, kitsZips)
        if kitNameInfo is None:
            #user skipped the kit
            continue
        # Kit Name & the filename string of the kit
        name, fileKitStr = kitNameInfo
        if not fileKitStr in kitsZips:
            kitsZips[fileKitStr] = Kit(name)
        kitType = GetKitType(file, name)
        kitsZips[fileKitStr].addFile(kitType, file)
    kits = {}
    for z in kitsZips:
        if kitsZips[z].name in kits:
            for type in kitsZips[z].files:
                if type not in kits[kitsZips[z].name].files:
                    kits[kitsZips[z].name].files[type] = []
                kits[kitsZips[z].name].files[type] += kitsZips[z].files[type]
        else:
            kits[kitsZips[z].name] = kitsZips[z]
    return kits;

def GetKitName(kit, kitsZips):
    #remove the end '-pp'
    kitStr = kit.rsplit("-", 1)[0]
    name = None
    goodInput = False
    while not goodInput:
        print()
        if kitStr in kitsZips:
            name = input("Please Enter Kit Name (default = " + kitsZips[kitStr].name + "): ")
            name = name or kitsZips[kitStr].name
            goodInput = True
            if name == "#skip":
                return None
        else:
            name = input("Please Enter Kit Name: ")
            if name == "#skip":
                return None
            if name is not "" :
                print()
                print("Entered Name = '" + name + "'")
                goodInput = misc.ConfirmInput("Is the name right?", True)
    return (name, kitStr)

def GetKitType(kit, kitName):
    #Remove file ext and get the ending -ep
    kitType = kit.rsplit(".")[0].rsplit("-", 1)[1]
    types = {1: "embellishment", 2: "alpha", 3: "paper", 4:"other"}
    defaultTypes = {"ep":1, "ap":2, "pp":3, "alpha": 2, "alphas": 2 }
    default = 1
    if kitType in defaultTypes:
        default = defaultTypes[kitType]
        print("Kit Type: ", kitType, " -> ", defaultTypes[kitType])

    while True:
        print()
        print("Please choose the type of this kit:")
        print(" 1) Embellishment")
        print(" 2) Alpha")
        print(" 3) Paper")
        print(" 4) Other")
        print()
        action = input("Please Select Number Above (default = " + types[default] + " ):")
        if action is "":
            return types[default];
        if action.isdigit():
            actionNum = int(action)
            if actionNum > 0 and actionNum < len(types)+1:
                return types[actionNum]



def ExtraKit(file):
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
