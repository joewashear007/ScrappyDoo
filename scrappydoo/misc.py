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

def ConfirmInput(question):
    print(question)
    print(" 0) No (default)")
    print(" 1) Yes")
    saveName = input("Please Enter Choice: ")
    return saveName.isdigit() and int(saveName) is 1
