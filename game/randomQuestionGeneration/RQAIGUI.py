import os
# Text length before status is printed
messageLen = 50
class RQAIGUI:
    def printHeader():
        print("\033[1;31;40m")
        os.system('cls')
        print(r"    ____  ____   ___    ____")
        print(r"   / __ \/ __ \ /   |  /  _/")
        print(r"  / /_/ / / / // /| |  / /  ")
        print(r" / _, _/ /_/ // ___ |_/ /   ")
        print(r"/_/ |_|\___\_/_/  |_/___/   ")        
        print("\033[1;37;40m")

    def printOk(message):
        while (len(message) < messageLen):
            message += " "
        message += "[\033[1;32;40mOK\033[1;37;40m]"
        print(message)

    def printLoaded(message):
        while (len(message) < messageLen):
            message += " "
        message += "[\033[1;33;40mLoaded\033[1;37;40m]"
        print(message)

    def printWarning(warning):
        print(f"\033[1;33;40mWarning: {warning}\033[1;37;40m")
    
    def printOptions():
        with open(os.path.join("Settings", "Requirements.ini")) as file:
            version = file.readline().split(": ")[1]
        print(f"RQAI version {version}")
        print("Option:    Result:")
        print("  -h         View this message")
        print("  -t         Perform AI training")
        print("  -b         Build the RQAI base")
        print("  -f         Build all RQAI base and training files")
    
    def printHelp():
        print("Command:   Result:")
        print("  help       View this message")
        print("  build      Build the RQAI base")
        print("  training   Perform AI training")
        print("  restore    Restore a past data backup")
        print("  daemon     Check for messages from the daemon")
        print("  exit       Exit the RQAI")