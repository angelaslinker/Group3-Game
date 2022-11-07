import sys
import os
from RQAIGUI import RQAIGUI
import subprocess
import sys
import pkg_resources

# Build the directories and files required to run the RQAI
fr = "Requirements.ini"
fct = "Category_Types.ini"
sDirectory = "Settings"

def writeRequirements():
    with open(os.path.join(sDirectory, fr,), "w") as f:
        contents = []
        contents.append("RQAI: 1.0.0")
        contents.append("")
        contents.append("Name: Py-Dictionary")
        contents.append("Version: 4.1.4")
        contents.append("Summary: Dictionary module")
        contents.append("Home-page: https://github.com/nit-in/py-dictionary")
        contents.append("")
        contents.append("Name: spacy")
        contents.append("Version: 3.4.2")
        contents.append("Summary: Industrial-strength Natural Language Processing (NLP) in Python")
        contents.append("Home-page: https://spacy.io")
        contents = "\n".join(contents)
        f.write(contents)
try: 
    os.mkdir(f"{sDirectory}")
    os.system("attrib +h " + f"{sDirectory}")
except:
    pass
finally:
    if os.path.isfile(os.path.join(sDirectory, fr)):
        pass
    else:
        open(os.path.join(sDirectory, fr), "x")
        writeRequirements()
    if os.path.isfile(os.path.join(sDirectory, fct)):
        pass
    else:
        open(os.path.join(sDirectory, fct), "x")

with open(os.path.join(sDirectory, fr)) as f:
    lines = f.readlines()
    requirements = {}
    lineNum = 0
for line in lines:
    if line.__contains__("Name: "):
        requirements[(line.split(": ")[1]).strip()] = lines[lineNum + 1].split(": ")[1].strip()
    lineNum += 1
for module, reqVersion in requirements.items():
    userVersion = 0
    try:
        userVersion = pkg_resources.get_distribution(f"{module}").version
        if (userVersion < reqVersion) & (userVersion > 0):
            print(f"User version is {userVersion} which is less than the required version of {reqVersion}. Update now? (Y/n)?", end= " ")
            subprocess.check_call(['pip', 'install', '-U', module])
        else:
            raise Exception(f"User version for {module} is invalid.")
    except:
        if (str(userVersion) < reqVersion):
            print(f"RQAI requires the {module} with version {reqVersion} to run. Download now? (Y/n)?", end= " ")
            userInput = input()
            if (userInput.lower().__contains__("y")):
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
            if (module == "spacy"):
                subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])

from RQAI import RQAI

class RandomQuestions:
    def __init__(self):
        _RQAI = None
        arguments = sys.argv
        if(arguments.__contains__("-h")):
            RQAIGUI.printOptions()
            os._exit(0)
        elif(arguments.__contains__("-b")):
            _RQAI = RQAI()
            _RQAI.Build()
        elif(arguments.__contains__("-t")):
            _RQAI = RQAI()
            _RQAI.AITraining()
        elif(arguments.__contains__("-f")):
            _RQAI = RQAI()
            _RQAI.Build()
            _RQAI.AITraining("build")
        else:
            _RQAI = RQAI()
        while(True):
            print(">>>", end=" ")
            userInput = input()
            if (userInput.lower().__contains__("help")):
                RQAIGUI.printHelp()
            elif(userInput.lower().__contains__("build")):
                _RQAI.Build()
            elif(userInput.lower().__contains__("training")):
                _RQAI.AITraining()
            elif(userInput.lower().__contains__("exit")):
                os._exit(0)

rq = RandomQuestions()