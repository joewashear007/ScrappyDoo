import os
import misc
import shutil
import subprocess
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
                goodInput = misc.ConfirmInput("Is '" + name + "' right?", True)
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
            print(e)
            print()
            print()
            print("We had issues extracting ", kitName)
            print("So we are going to kip it and move on...")
            print()
            print()


def MoveKitFolders(kits, current):
    misc.SetHeader("Moving Kits")
    dest = ""
    goodInput = False
    while not goodInput:
        print("Where should we move the kits?")
        print(" 1) Into the Personal Art Kits folder (Default)")
        print(" 2) I want to enter a custom folder")
        print(" 3) Skip this step")
        action = input("Please Select Number Above:")
        if action is "":
            homedir = os.path.expanduser("~")
            dest = os.path.join(homedir, "Documents", "Personal Art Kits")
            goodInput = True
        if action.isdigit():
            actionNum = int(action)
            if actionNum == 1:
                homedir = os.path.expanduser("~")
                dest = os.path.join(homedir, "Documents", "Personal Art Kits")
                goodInput = True
            if actionNum == 2:
                dest = misc.GetDir("Please enter the destination folder")
                goodInput = True
            if actionNum == 3:
                return
        if not goodInput:
            print()
            print("Hmm, that input seems wrong. Try again!")
            print()

    if not os.path.isdir(dest):
        dest = misc.GetDir(dest + " does not exist! Please enter a new destination folder")

    errors = []
    for name in kits:
        print("Moving ", name)
        try:
            shutil.move(os.path.join(current, name), dest)
        except Exception as e:
            errors.append(name)
            print()
            print("Error! Could Not move kit", name)
            print("Skipping the move for this kit")
            print()

    print("Done Moving Kits!")
    print("It is best to open Creative Memories to make sure all of the kits were installed properly")
    if len(errors)  > 0:
        print()
        print("===========================================================================")
        print("ERROR!!! There were errors, not all files mght have been copied")
        print("The following folders had errors")
        for name in errors:
            print(" * ", name)
        print("===========================================================================")
        print()
        print()
    misc.Pause()

def DeleteKitFiles(kits, folder):
    misc.SetHeader("Deleting Kits")
    print()

    for name in kits:
        for type in kits[name].files:
            for file in kits[name].files[type]:
                print("Deleting ", file)
                try:
                    os.remove(os.path.join(current, file))
                except Exception as e:
                    print("Error! Could not delete ", file)
                    print("Skipping... ")

    misc.Pause()
