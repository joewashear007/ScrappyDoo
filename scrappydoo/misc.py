import os

def Welcome():
    print()
    print(" .----. .---. .----.   .--.  .----. .----..-.  .-.   .----.  .----.  .----. ")
    print("{ {__  /  ___}| {}  } / {} \ | {}  }| {}  }\ \/ /    | {}  \/  {}  \/  {}  \\")
    print(".-._} }\     }| .-. \/  /\  \| .--' | .--'  }  {     |     /\      /\      /")
    print("`----'  `---' `-' `-'`-'  `-'`-'    `-'     `--'     `----'  `----'  `----' ")
    print()
    print()
    print("Welcome, this program will help you copy and install scrapbook zip files")
    print()
    Pause()
    os.system('cls' if os.name == 'nt' else 'clear')

def Pause():
    print()
    input("Please Press the 'Enter' key to continue...")

def ConfirmInput(question, yesDefault = False):
    while True:
        print(question)
        if( yesDefault):
            print(" 0) No")
            print(" 1) Yes (Default)")
        else:
            print(" 0) No  (Default)")
            print(" 1) Yes")
        option = input("Please Enter Choice: ")
        if option == "":
            return 1 if yesDefault else 0;
        if len(option) > 0 and len(option) < 2:
            if option.isdigit():
                return int(option) == 1
        else:
            print()
            print("Hmm, that input dosen't seem to be valid. Please try again")
            print()

def SetHeader(header):
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print()
    print(header)
    print("--------------------------------------------------------------------")
    print()


def GetDir(title):
    while True:
        print()
        print(title)
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
