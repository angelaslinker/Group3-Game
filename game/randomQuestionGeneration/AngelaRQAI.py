import os
import random
class AngelaRQAI():
    cDirectory = "Categories" # Folder where RQAI AI processing data is stored.
    oQDirectory = "randomQuestionGeneration\\Organized_Questions" # Folder that contains the sorted questions file.
    oQuestionsTxt = "OQuestions.txt" # File where the sorted questions are contained.
    qDirectory = "Questions" # Folder for user input of new, unsorted question files.
    sDirectory = "Settings" # Folder for the local settings that build the RQAI.
    bDirectory = "Backups" # Folder where the backup files associated with the Daemon are located.
    bFileLog = "Backups_Log.txt" # File where the backup log information for the Daemon is located.
    sfileCat = "Category_Types.ini" # Initialization file for the number of categories in the RQAI.
    def GetCategoryTypes(self):
        def GetCategoryTypes(self):
            options = [] # An array listing all of the categories in cDirectory.
            for item in os.listdir(self.cDirectory): # For every item in the cDirectory.
                options.append(item.split(".")[0]) # Adds the item from the cDirectory to the options array.
            return options # Returns options as a list.

    def GetRandomQuestionAndAnswers(self, category):
        dictionary = {} # Dictionary for the correct and false answers and question.
        with open(os.path.join(self.oQDirectory, self.oQuestionsTxt)) as file: # Opens the Organized Questions document:
            contents = file.readlines() # Copies the file to local memory
        if(contents.__contains__(f"{category}:\n")): # If contents contains the requested category:
            startIndex = contents.index(f"{category}:\n") + 1 # Mark the index of the next item (where the data starts).
            placeHolder = 0 # Placeholder to keep track of iterations.
            try: # Potentially accesses index that doesn't exist:
                while(len(contents[startIndex + placeHolder].split(" ")) > 1): # Check every line until the start of the next category is found.
                    placeHolder += 1 # Adds one to the placeholder.
            except IndexError: # Catch any potential indexErrors
                placeHolder -= 1 # The end of the array is back one space
            endIndex = startIndex + placeHolder # Map startIndex and placeHolder to endIndex.
            if (endIndex - startIndex < 4): # If less than four entries exist:
                print("Multiple choice has insufficient options.") # Print warning.
            val = random.randint(startIndex, endIndex) # Gets an item from the range of acceptabable values
            dictionary[contents[val].split(':')[0]] = contents[val].split(':')[1] # Adds the item with its corresponding answer to the dictionary.
            contents.remove(contents[val]) # Removes the question and answer from the contents
            endIndex -= 1 # Move the endIndex back one for the deleted question
            falseAnswers = self.RandAnswers(startIndex, endIndex, contents) # Get false answers from the helper method.
            falseAnswers = list(falseAnswers) # Make a list out of the set.
            for i in range(len(falseAnswers)): # For every item in the range:
                dictionary[f"{falseAnswers[i].split(':')[0]}{i}"] = falseAnswers[i].split(':')[1] # Add the item to the dictionary.
            return dictionary # Return the new dictionary.
        else: # The file contents don't contain the category:
            print(f"{category} category either does not exist or has no entries.") # Print output info
            return None # Return nothing.

    def RandAnswers(self, startIndex, endIndex, contents, answerSet=None):
        if (answerSet == None): # If set hasn't been created yet:
            answerSet = set() # Creates the set.
        answerSet.add(f"False answer:{contents[random.randint(startIndex, endIndex)].split(':')[1]}") # Adds the false answer to the set.
        if (len(answerSet) < 3): # If set is not yet three in length:
            return self.RandAnswers(startIndex, endIndex, contents, answerSet) # Calls the method again.
        return answerSet # Return the set.