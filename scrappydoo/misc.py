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
    print("Let's Get Started!")
    print()
    input("Please Press the 'Enter' key to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')

def ConfirmInput(question, yesDefault = False):
    print(question)
    if( yesDefault):
        print(" 0) No")
        print(" 1) Yes (Default)")
        saveName = input("Please Enter Choice: ")
        return len(saveName) == 0 or int(saveName) == 1
    else:
        print(" 0) No  (Default)")
        print(" 1) Yes")
        saveName = input("Please Enter Choice: ")
        return saveName.isdigit() and int(saveName) == 1
