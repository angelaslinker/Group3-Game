from RQAIGUI import RQAIGUI # Displays messages for the RQAI
import string # String manipulation
import os # File manipulation
from pydictionary import Dictionary # Definitions for words
import spacy # Sentence processing library
from datetime import datetime # Gets current date and time
import multiprocessing # Used to initialize the daemon

"""
RQAI performes word processing to group similar questions together.
"""
class RQAI:
    # These are the internal folders and files that the RQAI depends on.
    cDirectory = "Categories" # Folder where RQAI AI processing data is stored.
    oQDirectory = "Organized_Questions" # Folder that contains the sorted questions file.
    oQuestionsTxt = "OQuestions.txt" # File where the sorted questions are contained.
    qDirectory = "Questions" # Folder for user input of new, unsorted question files.
    sDirectory = "Settings" # Folder for the local settings that build the RQAI.
    bDirectory = "Backups" # Folder where the backup files associated with the Daemon are located.
    bFileLog = "Backups_Log.txt" # File where the backup log information for the Daemon is located.
    sfileCat = "Category_Types.ini" # Initialization file for the number of categories in the RQAI.
    categories = [] # The categories in the cDirectory.
    nlp = None # A reusable spacy module to keep the program from wasting space with allocation of new variables.
    connectionQ = None # The queue containing messages between RQAI and its daemon.

    """
    The initialization method checks through the local files to make sure that they exist, and then commits the local category files to memory. Also provides helpful messages to assist the user in avoiding errors.
    """
    def __init__(self):
        RQAIGUI.printHeader() # Initialization begins by checking all local files to ensure the program doesn't encounter errors with loading files that don't exist.
        self.GenerateFolders() # Checks all folders to make sure that they exist.
        self.GenOQTxt() # Checks the OQtxt file to make sure it exists.
        self.CheckCategory_Types() # Checks to make sure that the category files exist.
        q = multiprocessing.Queue() # Creating the communication queue for use between main program and the Daemon.
        self.connectionQ = q # Save connection with Daemon object to class level variable.
        with open(os.path.join(f"{self.sDirectory}", f"{self.sfileCat}")) as file:
            categories = file.readline().split(", ")
        self.categories = categories # Categories generated from the above accessed ini file.
        self.nlp = spacy.load("en_core_web_sm") # The core module that the spacy library uses to run in this program.
        # Below this line used for monitoring the progress of the RQAI initialization 
        count = 0                                                       
        for _ in os.listdir(self.cDirectory): # Gets a count of the total number of files in the cDirectory              
            count += 1     
        if (count == 0): # Warning messages assosciated with potential problems in the cDirectory1
            message = f"No files were found in the '{self.cDirectory}' directory, run the 'RQAI.build()' method to build the RQAI."
            RQAIGUI.printWarning(message)
        elif (count != len(categories)): # Note: The self.build method could be removed above to potentially cut down on load times for the RQAI, but hasn't been found to impact load times dramatically and so has been included by default.
            message = f"Size mismatch found, run the build option to fix RQAI."
            RQAIGUI.printWarning(message) 
        print("RQAI is ready to roll!") # RQAI Loaded successfully
            

    """
    AITraining handles the structure of the word processing that RQAI does. It makes a guess as to the category of phrase is fed into it, and then depending on the signature that's given to it either records that guess or allows for human correction before recording the guess.
    """
    def AITraining(self, arg=""): 
        # Create key map
        keyMap = {} # The key map is a list of the number of files in the cDirectory with a number assigned to it to use for the human entry
        count = 0
        for filename in os.listdir(self.cDirectory):                     
            keyMap[filename.split(".")[0]] = count
            count += 1
        # End key map creation
        questionsCount = 0
        for filename in os.listdir(self.qDirectory): # Capable of reading multiple different files in the Questions directory.
            qContents = [] 
            tempContents = []
            questionsCount += 1
            if (arg != "build"): # Part of TODO: enable the AI to make decisions automatically.
                print(f"Would you like to train with {filename}? (Y/n)?", end = " ") # Enables the user to choose for each file whether or not to train with that file.
                if (input().lower().__contains__("y")):
                    with open(os.path.join(self.qDirectory, filename ), "r") as file: # Reads through qDirectory chosen file and commits it to local memory
                        qContents = file.readlines()
                    for question in qContents: # Reads through EVERY LINE in the questions document and asks the user to make decisions based off of those lines.
                        defintionSet = self.GetQuestionSet(question) # Gets the words that go into the category files, these words are the definitions of the subjects of the question.
                        guess = self.GuessQuestion(defintionSet) # Makes a guess looking for similar words in the category files and then returns the highest match.
                        guessLocation = keyMap.get(guess) # Used for UI coloring, the guessLocation is the order that the location file appears in the file
                        print("    ", end="") # tab
                        print(f"{question.strip()}") # Prints the question that the program is currently examining without the \n
                        print("    ", end="") # tab
                        print(f"This looks like a \033[1;{(guessLocation % 6) + 31};40m{guess}\033[1;37;40m question. Press enter to input the question into the database as a {guess} question or enter a number for a different question type:") # AI guess
                        types = ""
                        for type, num in keyMap.items():
                            if (types != ""):
                                types += ", "
                            types += f"(\033[1;{(num % 6) + 31};40m{type}: {num}\033[1;37;40m)"
                        types += " or enter 'exit' to finish training." 
                        print(types) # Prints out the keymap with the according file names as the options for recording the question.
                        print(">>> ", end="") # UI
                        entry = ""
                        uI = input() # Get user input.
                        if (uI == ""): # If UI blank:
                            entry = guess
                        elif(uI == "exit"): # If UI is 'exit':
                            break;
                        else: # Otherwise a character has been input.
                            loop = True # loop variable to protect against bad input.
                            while(loop): # Until good input is reached:
                                try:
                                    uI = int(uI) # Tries to get an integer from user input.
                                    entry = list(keyMap.keys())[list(keyMap.values()).index(uI)] # Tries to get the assosciated key from user input.
                                    loop = False
                                except:
                                    print(types) # Repeat question
                                    uI = input() # Repeat input
                        tempContents.append(question) # Adds the question to tempContents to use with removing questions from the qDirectory accessed file
                        with open(f"{self.oQDirectory}/{self.oQuestionsTxt}", "r") as f:
                            contents = f.readlines() # Get the contents of the organized question file
                        if (contents.__contains__(f"{entry}:\n")): # If contents contain question already do nothing
                            pass
                        else:
                            contents.append(f"{entry}:\n") # Contents don't contain question so append question to the end of the document
                        contents.insert(contents.index(f"{entry}:\n") + 1, question) # Inserts new question after the category heading
                        _tempContents = contents # Second _tempContents file to help with formatting issues where \n could potentially overtake document.
                        for item in contents: # Pulls every question from oQuestions.
                            _tempContents[_tempContents.index(item)] = item.strip() # Remove any newlines
                            if(item == ""): # Stop buildup of newlines
                                _tempContents.remove(item) 
                        contents = _tempContents # Copies newline-less _tempContents to contents.
                        with open(f"{self.oQDirectory}/{self.oQuestionsTxt}", "w") as f:
                            contents = "\n".join(contents) # Joines newline-less lines with newlines before writing contents to file.
                            f.write(contents) # Writes contents to file
                        self.AddCategoriesTxt(defintionSet, entry) # Adds the definition set that was used earlier to the category files that were assigned by the entry
                for item in tempContents: # Takes any questions that the user read from the questions file and removes them from the read file in the qDirectory
                    qContents.remove(item) 
                file = open(os.path.join(self.qDirectory, filename ), "w") # Opens the qDirectory accessed file with write permissions
                file.writelines(qContents) # Writes new contents
        if (questionsCount == 0): # If no files wre found in qDirectory:
            message = "No files were found in the Questions folder."
            RQAIGUI.printWarning(message)

    """
    The GenerateFolders method checks to make sure that the folders that the program is dependent on exist, and if they do not will create them with their needed attributes.
    """
    def GenerateFolders(self): 
        print("Checking directory dependencies:")
        try:
            os.mkdir(self.cDirectory) # Makes the Categories directory
            os.system("attrib +h " + self.cDirectory)
            message = (f"{self.cDirectory} was created successfully.")
            RQAIGUI.printLoaded(message)
        except:
            message = (f"{self.cDirectory} folder exists.")
            RQAIGUI.printOk(message)
        try: 
            os.mkdir(self.oQDirectory) # Makes the Organized Questions directory
            os.system("attrib +h " + self.oQDirectory)
            message = (f"{self.oQDirectory} was created successfully.")
            RQAIGUI.printLoaded(message)
        except:
            message = (f"{self.oQDirectory} folder exists.")
            RQAIGUI.printOk(message)
        try: 
            os.mkdir(self.sDirectory) # Makes the Settings directory
            os.system("attrib +h " + self.sDirectory)
            message = (f"{self.sDirectory} was created successfully.")
            RQAIGUI.printLoaded(message)
        except:
            message = (f"{self.sDirectory} folder exists.")
            RQAIGUI.printOk(message)        
        try: 
            os.mkdir(self.bDirectory) # Makes the Backup directory
            os.system("attrib +h " + self.bDirectory)
            message = (f"{self.bDirectory} was created successfully.")
            RQAIGUI.printLoaded(message)
        except:
            message = (f"{self.bDirectory} folder exists.")
            RQAIGUI.printOk(message)
        try:
            os.mkdir(self.qDirectory) # Makes the Questions directory
            message = (f"{self.qDirectory} was created successfully.")
            RQAIGUI.printLoaded(message)
        except:
            message = (f"{self.qDirectory} folder exists.")
            RQAIGUI.printOk(message)
        
    """
    The Build method is responsible for making the needed files in the Categories folder based off the categories in the Settings/Category_Types.ini
    """
    def Build(self):
        files = [] # Keeps track of the files that already exist.
        for filename in os.listdir(self.cDirectory): # For every file in the cDirectory:
            files.append(filename) # Add the filename to the files list.
        addCount = 0
        for type in self.categories: # For every category_type in the local categories variable:
            f = os.path.join(self.cDirectory, type)
            if os.path.isfile(f"{f}.txt"): # If the file from the local list exists in the directory already.
                message = (f"{f} file exists.") # Print that the file exists.
                RQAIGUI.printOk(message) # Print the RQAIGUI OK message.
                files.remove(f"{type}.txt") # Remove from the list of files that are still needed.
            else: # The file doesn't exist:
                open(f"{f}.txt", "x") # Creates the file.
                file = open(f"{f}.txt", "w") # Populates the document with the needed header format.
                file.write("[RQAIV]:0") # RQAI Value Keeps track of total words in document.
                message = (f"{type}.txt was created successfully.") 
                RQAIGUI.printLoaded(message) # Print the file loaded message.
                addCount += 1
        if (addCount != 0): # If any files were added
            print(f"{addCount} file(s) added in total to training list.") # Prints the total number of lists that were made.
            message = "New files require AI training before RQAI can use them." # Prints the AI training warning message.
            RQAIGUI.printWarning(message)
        rmvCount = 0
        for filename in files: # For any files that are still in the file list
            file = os.path.join(self.cDirectory, filename)
            loop = True
            while(loop): # Prevent bad input
                try:
                    message = f"Found extra file at path {file}. Remove file? (Y/n)?" # Asks the user if he wants to remove the extra file
                    RQAIGUI.printWarning(message)
                    uI = input().lower()
                    if (uI.__contains__("y")): # If user input contains 'y':
                        os.remove(f"{file}") # Remove the file from the categories folder
                        rmvCount += 1
                    loop = False # Break the loop
                except:
                    pass
        if (rmvCount != 0): # If any files were removed:
            print(f"{rmvCount} file(s) removed in total from training list.") # Print how many files were removed
    
    """
    The CheckCategory_Types method makes sure that the Settings/Category_Types.ini file exists and creates it if it does not.
    """
    def CheckCategory_Types(self):
        if os.path.isfile(os.path.join(self.sDirectory, self.sfileCat)): # If path is valid:
            message = f"{self.sfileCat} file exists."
            RQAIGUI.printOk(message)
        else:
            open(os.path.join(self.sDirectory, self.sfileCat), "x") # Else create file:
            message = f"{self.sfileCat} was created successfully."
            RQAIGUI.printLoaded(message)

    """
    The GenOQTxt method makes sure that the Organized_Questions/OQuestions.txt file exists and creates it if it does not.
    """
    def GenOQTxt(self):
        if os.path.isfile(f"{self.oQDirectory}/{self.oQuestionsTxt}"): # If path is valid:
            message = (f"{os.path.join(self.oQDirectory, str(self.oQuestionsTxt)).split('.')[0]} file exists.")
            RQAIGUI.printOk(message)
        else:
            open(f"{self.oQDirectory}/{self.oQuestionsTxt}", "x") # Else create the file:
            message = (f"{self.oQuestionsTxt} was created successfully.")
            RQAIGUI.printLoaded(message)

    """
    GetQuestionsSet controls the structure of the definition set. GQS first gets a list of nouns from the question it's provided with, then gets the definitions for each of those nouns and returns them as a set so that no duplicates are present.
    """
    def GetQuestionSet(self, question):
        questionNP = question.translate(str.maketrans('', '', string.punctuation)) # Removes punctuation from question
        dict = Dictionary # Generates the local dictionary to be used.
        definitionSet = {"init"} # Frequency of words in definition is omitted.
        definitionSet.remove("init") # Removes the supplied word so that data structure is recognized as a set and is empty.
        subjects = self.GetSubj(questionNP) # Gets the subjects of question.
        for word in subjects: # For every word in the subjects list:
            dict = Dictionary(word, 1) # Dictionary definition for each word in subject.
            for i in dict.meanings()[0].translate(str.maketrans('', '', string.punctuation)).split(" "): # Splits definition by spaces and removes all punctuation so that "the" and "the." are the same.
                if ((len(i) > 2) & ((i != "and") & (i != "the"))): # Removes small words like "if" and "of" as well as "and" and "the".
                    definitionSet.add(i.lower()) # Add remaining words to set.
        return definitionSet # Returns the set.

    """
    GuessQuestion is the AI's tool to compare the current set of words to other sets to make an educated decision about which category the set belongs in.
    """
    def GuessQuestion(self, definitionSet):
        matchPercentage = {} # Holds both the category types as well as the percentage to how similar the definitionSet is to the category.
        for filename in os.listdir(self.cDirectory): # For every file in the cDirectory
            path = os.path.join(self.cDirectory, filename)
            with open(f"{path}", "r") as f: # Open the path to the selected file in the cDirectory.
                contents = f.readlines() # Copies the contents of the files to a new local instance 
                amount = 0 # Words that match the words provided by the definitionSet
                for val in definitionSet: # for every value in the definitionSet:
                    dSet = self.BstIndex(contents, val) # Lookup of the val from definitionSet to see if the value is in the file
                    found, position = dSet.items() # Unpacks the dictionary that was returned
                    if (found[1]): # Checks "found" value from the dictionary
                        amount += int(contents[position[1]].strip().split(":")[1]) # Item was found, add the number of word occurences to amount.
                totalWordCount = int(contents[0].split(":")[1]) # TotalWordCount is [RQAIV] val
                if (totalWordCount == 0): # The document has no words so don't make a divide by 0 error:
                    matchPercentage[filename.split(".")[0]] = 0 # Return 0
                else: # The document is populated so apply the formula:
                    matchPercentage[filename.split(".")[0]] = (100 * amount/totalWordCount) # The percentage to which the file contents match the definitionSet contents.
        highestVal = 0 # Instantiate variables 
        highestKey = 0 # Instantiate variables
        for key, val in matchPercentage.items(): # For every value in the matchPercentage definitionSet:
            if (val >= highestVal): # If value is greater than or equal to highestKey replace highest with these values.
                highestKey = key # Update highestKey
                highestVal = val # Update highestVal
        return highestKey # Returns the category which matches the definitionSet the best.

    """
    GetSubj is responsible for returning the subjects that are nouns in the phrase that is passed to it.
    """
    def GetSubj(self, question): # The method to get the subjects using the Spacy module.
        qnlp=self.nlp(question) # Instantiate the Spacy nlp instance with provided question.
        nSubjArray = [nSubj for nSubj in qnlp if (nSubj.dep_ == "nsubj")] # add nSubj to the nSubjArray if part of speech in qnlp is defined as a "nsubj".
        return nSubjArray # Return the subjects from the phrase.
    
    """
    AddCategoriesTxt is responsible for populating the category.txt documents with the items from the dictOutput to the provided category. Writes category files in the format of word[0], occurences[1], signature[2], time[3].
    """
    def AddCategoriesTxt(self, dictOutput, category, signature="sys"):
        dateAndTime = datetime.now() # The time when this method was called
        dt_string = dateAndTime.strftime("%Y.%m.%d.%H.%M.%S") # Reformats the date and time in a way that's more useful for the RQAI.
        with open(f"{self.cDirectory}/{category}.txt", "r") as f: # Opens the document for the specified category.
            contents = f.readlines() # Copies document contents for the specified category from the document to a local variable. 
        tempContents = contents # Makes a version of contents that we can work with and not ruin the for loop using contents.
        wordContents = [] # Contents, but just the words, nothing after the first ':'
        for item in contents: # For every line in contents 
            wordContents.append(item.split(':')[0]) # Builds wordcontents as per the above defined requirements.
            tempContents[tempContents.index(item)] = item.strip() # Removes any newlines from tempContents.
            if(item == ""): # Stop buildup of newlines
                tempContents.remove(item) # Removes any blank lines which were previously just a \n 
        contents = tempContents # Corrects contents to be the non-blank lines contents to avoid errors below.
        for word in dictOutput: # For every word in the provided definition set:
            lookupDict = self.BstIndex(contents, word) # A set containing the lookup information that's created by BstIndex.
            found, position = lookupDict.items() # Unpack the BstIndex set.
            if (found[1]): # If item was found:
                signatureOld = contents[position[1]].split(':')[2] # Gets the old signature.
                if (signature == signatureOld): # If both entries were made by the same author:
                    timeSignatures = int(contents[position[1]].split(':')[1]) # Gets the number of time signatures.
                    time = "" # Instantiate time variable
                    for t in range(timeSignatures): # For each time signature
                        time += f"{contents[position[1]].split(':')[3 + t]}:" # Copies old time signatures.
                    time += dt_string # Adds current dt_string signature to old time signatures.
                    contents[position[1]] = (f"{contents[position[1]].split(':')[0]}:{(int(contents[position[1]].strip().split(':')[1]).__add__(1))}:{signatureOld}:{time}") # Increases the item's value by one.
                else: # The entries were made by different authors:
                    spot = position[1] + 1 # Checks spots starting after the current position.
                    added = False # Variable to keep track of whether or not an addition has been made. 
                    for i in range(2): # Checks for multiple different signatures, since only three are available (man, sys, ans) there are only two checks left to make.
                        if (spot + i < len(contents)): # If we haven't gone past the length of the contents array
                            if((contents[spot + i].split(':')[0] == word) & (contents[spot + i].split(':')[2] == signature)): # If the line word and signature match the current word and signature
                                timeSignatures = int(contents[spot + i].split(':')[1]) # Gets the number of time signatures.
                                time = "" # Instantiate time variable
                                for t in range(timeSignatures): # For each time signature
                                    time += f"{contents[spot + i].split(':')[3 + t]}:" # Copies old time signatures.
                                time += dt_string # Adds current dt_string signature to old time signatures.
                                contents[spot + i] = (f"{contents[spot + i].split(':')[0]}:{(int(contents[spot + i].strip().split(':')[1]).__add__(1))}:{signature}:{time}") # Increases the item's value by one.
                                added = True # A value was added.
                    if (not added): # No value has been added so add it at the found position.
                        contents.insert(position[1], f"{word}:1:{signature}:{dt_string}") # Inserts new item at appropriate location.
            else: # Item wasn't found:
                if (position[1] >= len(contents)): # If location is at the end of the list:
                    contents.append(f"{word}:1:{signature}:{dt_string}") # Append rather than insert to avoid errors.    
                else: # Item wasn't found at the end of the list
                    if (contents[position[1]].split(':')[0] < word): # The item is at the end of the list but position couldn't be moved to the end of the list.
                        contents.append(f"{word}:1:{signature}:{dt_string}") # Append rather than insert to avoid errors.    
                    else: # Item is somewhere in the middle of the list:
                        contents.insert(position[1], f"{word}:1:{signature}:{dt_string}") # Inserts new item at appropriate location.
            contents[0] = f"{contents[0].split(':')[0]}:{(int(contents[0].split(':')[1]).__add__(1))}" # Updates the [RQAIV] information
        with open(f"{self.cDirectory}/{category}.txt", "w") as f: # Opens the category file with write permissions:
            contents = "\n".join(contents) # Concatenate items together with \n's
            f.write(contents) # Writes the contents to the category file.

    """
    BstIndex controls the BstInternal method, calls the recursive method with the values determined here in the BstIndex. Efficiency is available below.
    """
    def BstIndex(self, array, val): # Modified BST to require as few lookups as possible for this program. Because this isn't a true bst with nodes there has to be an end condition where the computer searches through the remaining items, else an endless loop can occur. As the dataset approaches infinity the limit of lookups approaches log(n) + 10 + 1000/n. BST won't start dividing values until the dataset is larger than 37.016.
        return self.BstInternal(array, val, 1, len(array), round(1000/len(array))) # Returns the dictionary output of BstInternal.

    """
    BstInternal aims to cut the document down to a size that provides as few readings as necessary without entering an infinite loop looking for items that don't exist. Takes a target size to cut the document down to, and then reads through the remaining values until the val or a larger val is found, whichever happens first.
    """
    def BstInternal(self, array, val, bottom, top, endCondition): # Efficiency is more complex than the overview given in BstIndex, some repeat values are allowed which means that the number of calls could exceed what were listed above by a factor of three (for each signature type), but this would be rare.
        pos = int((top+bottom)/2) # Position is located at the middle of the document
        if (abs(top - bottom) <= endCondition): # If remaining document size is less than or equal to the endcondition value:
            pos = bottom # Position is at the document's currently defined bottom
            dict = {} # Return dictionary for found values
            dict["Found"] = False # Sets Found to 'False' by default
            for i in range(len(array)-bottom): # For currently defined bottom to top.  
                pos = bottom + i # Current position is bottom + loop iteration
                if (array[pos].split(':')[0] == (val)): # Value is in document:
                    dict["Found"] = True # Update dictionary value for Found.
                    break # End search.
                elif val < array[pos].split(":")[0]: # Value is now less than read value:
                    break # End search.
            dict["Position"] = pos # Position information where spot was found or passed.
            return dict # returns the INDEX of the value and whether or not spot was found.
        if array[pos].split(':')[0] == (val): # Item was found during Bst splits
            dict = {} # Return dictionary for found values
            dict["Found"] = True # Item was found
            dict["Position"] = pos # Location item was found
            return dict # returns the INDEX of the value and whether or not spot was found.
        elif array[pos] > val: # Document value is larger than currently read value:
            return self.BstInternal(array, val, bottom, pos - 1, endCondition) # Read everything above (lower than) the current value
        else: # Document value is less than currently read value:
            return self.BstInternal(array, val, pos + 1, top, endCondition) # Read everything below (higher than) the current value

    """
    The aim of the Rollback method is to correct bad additions to the RQAI. Instead of deleting the whole document that RQAI uses, it will peel it back, layer by layer based off of the date and time of items that were added to it.
    """
    def Rollback(self, target, dateTime, signature="all"): # This method will take a long time to run!
        with open(os.join.path(self.cDirectory, f"{target}.txt"), "r") as file:
            contents = file.readlines() # Commits the target file to local memory.
        skipLine = True # Enables the first line [RQAIV] to be skipped.
        for line in contents: # For every line in the contents file:
            if (skipLine): # If line is flagged to be skipped.
                skipLine = False # Trip the flag to skip the line.
                continue # Skips to the next line in the loop.
            items = line.split(':') # Divides the line into an array by splitting around the ':' character
            itemsRemoved = 0 # Variable to keep track of the number of items deleted from the items array
            if ((items[2] == signature) | signature == "all"): # If the targeted signature is found
                pass # Continue on with the deletion process.
            else: # The targeted signature was not found:
                continue # Skip to the next item in the array.
            for i in range(len(items) - 3): # A loop to check through all the time signatures.
                if (items[i + 2] > dateTime): # Checks to see if item dateTime is larger than the dateTime specified (needs to be removed).
                    itemsRemoved = len(items) - 3 - i # The number of items removed is equal to the total number items minus the first three, minus the for loop iteration.
                    items[i + 2] = "ROLLBACK" # Marks the spot for removal.
            items[1] = int(items[1]) - itemsRemoved # Changes the number of occurences of the word.
            contents[0] =  f"{contents[0].split(':')[0]}:{int(contents[0].split(':')[1]) - itemsRemoved}" # Updates the RQAI value to reflect the number of items that were removed. 
            tempItems = [] # Spot to hold the new line in separate array indices.
            for i in range(len(items)): # For every spot in the items array
                if (items[i] != "ROLLBACK"): # If the spot is not marked for rollback then continue appending items onto the array:
                    tempItems.append(items[i]) # append the item.
                else: # The spot is marked for rollback
                    break # Stop the loop to add new items.
            newLine = ':'.join(tempItems) # Joins the tempItems array together into a new line.
            line = newLine # Updates the line with the new values.
        with open(os.join.path(self.cDirectory, f"{target}.txt"), "w") as file:
            file.writelines(contents) # Writes the array contents onto the target file.

"""
The goal of the RQAIDaemon object is to maintain the integrity of RQAIs work. Designed for the RQAI class to do the creation of this object.
"""
class RQAIDaemon:
    # Objects that the RQAI uses that the daemon also needs access to
    cDirectory = None # For verifying data integrity.
    connectionQ = None # Multiprocessing shared memory object.
    bDirectory = None # The directory where the daemon's backup work is contained.
    bFileLog = None # The log file for the daemon's backup work.

    """
    The __init__ method serves as the entry point to the daemon where it will begin its daemonic tasks.
    """
    def __init__(self, cDirectory, connectionQ, bDirectory, bFileLog):
        self.cDirectory = cDirectory # Copy the RQAI cDirectory to Daemon's memory
        self.connectionQ = connectionQ # Copy the RQAI connectionQ object to Daemon's memory
        self.bDirectory = bDirectory # Copy the RQAI bDirectory to Daemon's memory
        self.bFileLog = bFileLog # Copy the RQAI bFileLog file to Daemon's memory
        currentFile = 0 # Count for the spot currently being read in the file list
        count = 0 # Count for total number of files                      
        for filename in os.listdir(self.cDirectory): # Gets a count of the total number of files in the cDirectory              
            count += 1 # Adds one to total file list.                 
        for filename in os.listdir(self.cDirectory): # Loads the files in the cDirectory and commits them to local memory.               
            currentFile += 1 # Adds one to the loading variable for the current number of the file's load order                  
            if (self.VerifyFileIntegrity(filename)): # Reading the RQAI Files and committing them to local memory
                self.connectionQ.put(f"File verified ({currentFile}/{count})") # UI information
        self.DaemonEntry() # Begin daemon tasks.       

    """
    DaemonEntry serves as the program control for the Daemon, assigning its tasks and controlling the flow of the program.
    """
    def DaemonEntry(self):
        self.BackupData() # Check to make sure data is ready to be used

    """
    BackupData is the Daemon's way of making sure that the valuable data of the program is preserved against manual input errors, or any other kind of data error that may occur. Instantiating this class using multiprocessing creates a daemon that runs in the background.
    """ 
    def BackupData(self):
        if not (os.path.exists(os.path.join(self.bDirectory, self.bFileLog))): # Checks to see if log file path exists:
            open(os.path.join(self.bDirectory, self.bFileLog), "x") # If file doesn't exist creates the file.
            message = (f"{self.bFileLog} was created successfully.") # Output message
            self.connectionQ.put(message) # Sends a message that the file was created to the multiprocessing queue.
        else: # Log file does exist
            message = (f"{self.bFileLog} file exists.") # Output message
            self.connectionQ.put(message) # Sends a message that the file was created to the multiprocessing queue.
        for item in os.listdir(self.cDirectory): # For every item in the cDirectory
            backupItem = 0 # The date of the file verification
            with open(os.path.join(self.cDirectory, item)) as file: # Opens the subject file for reading
                contents = file.readlines() # Copies the file contents to an array
            try: 
                if (contents[0].split(':')[2] == "verified"): # Attempts to read a spot that may not exist
                    backupItem = contents[0].strip().split(':')[3].split('.') # Gets the verification date
                    fArray = [backupItem[0], backupItem[1], backupItem[2]]
                    folderName = ".".join(fArray) # Constructs folder name from verification info
                    newFileName = f"{item.split('.')[0]}.{'.'.join(fArray)}.txt"
                    if not (os.path.isdir(os.path.join(self.bDirectory, folderName))): # If the folder for the day doesn't already exist:
                        os.mkdir(os.path.join(self.bDirectory, folderName)) # Make the folder.
                    if not os.path.exists(os.path.join(self.bDirectory, folderName, newFileName)): # If the backup item doesn't already exist
                        open(os.path.join(self.bDirectory, folderName, newFileName), 'x') # Create the backup item
                        with open(os.path.join(self.bDirectory, folderName, newFileName), 'w') as newFile: # Open the newly created backup item
                            newFile.writelines(contents) # Write the old file contents to a new file. TODO: Copy file instead of copying contents
                        with open(os.path.join(self.bDirectory, self.bFileLog), 'r') as log: # Opens the system log file
                            contents = log.readlines() # Copies the log files into a local array
                        if (contents.__contains__(folderName + "\n")): # Searches through the array to find if the folder exists already:
                            indexOf = contents.index(folderName + "\n") # Folder already exists, grabs its index.
                            if not (indexOf + 1 >= len(contents)): # Make sure that we aren't trying to add data to a spot that doesn't exist
                                contents.insert(indexOf + 1, f"{newFileName}:{f'{os.path.getsize(os.path.join(self.bDirectory, folderName, newFileName))}'} bytes") # Insert new item
                            else: # We're at the end of the list
                                contents.append(f"{newFileName}:{f'{os.path.getsize(os.path.join(self.bDirectory, folderName, newFileName))}'} bytes") # Appends rather than inserts the new value
                        else: # The folder entry doesn't already exist
                            contents.append(folderName) # adds the folder name to the file
                            contents.append(f"{newFileName}:{f'{os.path.getsize(os.path.join(self.bDirectory, folderName, newFileName))}'} bytes") # Appends the entry onto the file
                        newContents = []
                        for item in contents:
                            newContents.append(item.strip() + "\n")
                        with open(os.path.join(self.bDirectory, self.bFileLog), 'w') as log: # Opens the system log file
                            log.writelines(newContents)
            except IndexError as e: # Catch previously defined error of accessing a spot that may not exist
                self.connectionQ.put(f"Index error was reached : {e}") # File wasn't ready to be read, add the error to the multiprocessing shared memory object.
    
    """
    VerifyFileIntegrity checks through a category file and makes sure that the file contains the correct number of signatures as well as that the total number of items matches so that the AI work that this program does is as accurate as possible.
    """        
    def VerifyFileIntegrity(self, filename):
        f = os.path.join(self.cDirectory, filename)
        if os.path.isfile(f): # Checks to see if file at filename is file (it had better be)
            with open(f) as file: # If that file exists opens it.
                contents = file.readlines() # Copies the file contents to a local variable.
            total = 0 # Total number of entries for the file.
            flag = False # Flag to let the user know if anything unexpected was encountered.
            if (not(contents[0].split(':')[0] == "[RQAIV]")): # Checks to make sure header is correct:
                flag = True # If not correct flip flag.
            for i in range(len(contents) - 1): # For every item in contents besides the header:
                try:
                    spot = i + 1 # Starts at the first spot and updates every item after.
                    tempContents = contents[spot].split(':') # Copies the line into a local array.
                    size = int(tempContents[1]) # The size is found in the second array indice.
                    total += size # Total is increased by size.
                    for c in range(size): # Loop for every expected date item.
                        tempContents[c + 3] = "Accessed" # States that the item was read correctly.
                    for c in range(len(tempContents) - 3): # Loop for every date item.
                        if tempContents[c + 3] != "Accessed": # If item hasn't been accessed:
                            flag = True # Flips the flag.
                except IndexError: # Catches IndexErrors caused by accessing items that don't exist (size was too large)
                    flag = True # Flips the flag.
            if (total != int(contents[0].split(':')[1])): # If total doesn't match the RQAIV total:
                flag = True # Flips the flag.
            if (flag): # If the flag has been flipped at any point:
                message = f"Formatting error found in the following document: {filename}" # Notify the user that there's an error in the document.
                RQAIGUI.printWarning(message) # Prints the message.
                return False # File contains errors
            else: # File doesn't contain errors
                with open(f, "r") as file: # Open file with reading permissions.
                    contents = file.readlines() # Copy contents to an array.
                with open(f, "w") as file: # Open file with read permissions
                    rqaivLine = contents[0].split(':') # Split the contents by the ':' character
                    dateAndTime = datetime.now() # The time when this method was called
                    dt_string = dateAndTime.strftime("%Y.%m.%d.%H.%M.%S") # Reformats the date and time in a way that's more useful for the RQAI.
                    if (len(rqaivLine) > 2): # If the heading information already exists:
                        rqaivLine[2] = "verified" # Reupdate the header in array indice[2].
                        rqaivLine[3] = dt_string + "\n" # Reupdate the header in array indice[3].
                    else: # The header doesn't exist:
                        rqaivLine[1] = rqaivLine[1].strip() # Clean the newline off of rqaivLine[1]
                        rqaivLine.append("verified") # Add the header information to array indice[2].
                        rqaivLine.append(dt_string + "\n") # Add the header information with formatting to array indice[3].
                    contents[0] = ":".join(rqaivLine) # Join the contents together using RQAI encoding.
                    contents = ("").join(contents) # Joins all the contents together into a single string
                    file.writelines(contents) # Writes all the lines of the edited contents array to the file.
                    return True

# The area below is used for debugging and should be empty, if it is not empty it is recommended to clear it.