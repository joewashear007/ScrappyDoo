import os
import misc
from kit import Kit

def ProcessKits(kitFiles):
    kitsZips = {}
    for x, file in enumerate(kitFiles):
        misc.SetHeader("Get Kit Information ("+ str(x + 1) + " of " + str(len(kitFiles)) + ")")
        print("To skip a file, please enter '#skip' for the name")
        print()
        print()
        print("Current File: ", file)
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
    # Conbine kits by Name
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
                goodInput = misc.ConfirmInput("Is the '" + name + "' right?", True)
    return (name, kitStr)

def GetKitType(kit, kitName):
    #Remove file ext and get the ending -ep
    kitType = os.path.splitext(kit)[0].rsplit("-", 1)[1]
    types = {1: "embellishment", 2: "alpha", 3: "paper", 4:"other"}
    defaultTypes = {"ep":1, "ap":2, "pp":3, "alpha": 2, "alphas": 2 }
    default = 1
    if kitType in defaultTypes:
        default = defaultTypes[kitType]

    while True:
        print()
        print("Please choose the type of this kit:")
        print(" 1) Embellishment", " (Default) " if default == 1 else "")
        print(" 2) Alpha", " (Default) " if default == 2 else "")
        print(" 3) Paper", " (Default) " if default == 3 else "")
        print(" 4) Other", " (Default) " if default == 4 else "")
        print()
        action = input("Please Select Number Above:")
        if action is "":
            return types[default];
        if action.isdigit():
            actionNum = int(action)
            if actionNum > 0 and actionNum < len(types)+1:
                return types[actionNum]



def ExtractKits(kits, current):
    misc.SetHeader("Extracting Kits, Please Wait ...")
    for kitName in kits:
        try:
            kits[kitName].extract(current, current)
        except Exception as e:
            print()
            print()
            print("We had issues extracting ", kitname)
            print("So we are going to kip it and move on...")
            print()
            print()
