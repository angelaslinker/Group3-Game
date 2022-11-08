# RQAI
This is a word processing program that's capable of automatically growing with a dataset. The RQAI's goal is to take phrases, sentences, questions, answers or any bit of text and group like bits of text into files or 'categories', storage containers for the RQAI values.

## Files
RQAI handles the creation and manipulation of several documents. All of these files can be deleted and automatically regenerated in the need of a hard reset with the data. Some of these files are needed to use RQAI to it's fullest ability and others aren't meant to be touched by anyone but the program. An outline of the files is listed below:
Directory: Categories (hidden)
    Sub-file: Category_text_documents (AI only)
Directory: Organized_Questions (hidden)
    Sub-file: OQuestions (AI only)
Directory: Questions (visible)
    '(This spot is where input data files are to be fed)'
Directory: Settings (hidden)
    Sub-file: Category_Types.ini (The categories list, meant to be edited. All categories must be seperated by a comma and space: ', ')
    Sub-file: Requirements.ini (Used by the Standalone for initialization)

Categories files contain the largest amount of technical information which the system relies on as part of its decision making process. The RQAI will record in the category documents different sections broken up by a ":" character. The first section contains a word that was found as part of a subjects definition. The second section contains a count of the frequency of which this character has been found. The third section contains the signature of who added the information to help in complex sorting. The fourth and all subsequent sections contain the dates of when each occurence of the word was added.

## Classes
### RQAI Class
The RQAI class handles all the file creation/management this program does, as well as the training of the AI.

#### Standalone.py
The Standalone.py file is meant to serve as an installer and an entry point for the program when another main class isn't present. The standalone allows for command line arguments to be run and will give interactive instruction to how to set up the program. In the event of any missing modules that are needed and aren't included in the python3 base by default the Standalone will offer to download the needed modules to ensure that RQAI runs smoothly. RQAI is not dependent on the Standalone for functionality, however.

#### RQAIGUI.py
The RQAIGUI.py file serves as a simple graphical user interface. While limited the graphical user interface does provide help menus and functionality to further guide the unpracticed user to be able to make use of the RQAI.

#### RQAI.py
The RQAI.py file is the heart of this program, and serves to handle all of the wordprocessing needed to make this AI functional. The program searches for the noun subjects in a sentence via the spacy module, then retrieves the dictionary definitions of those words via the py-dictionary module, and finally records the words and questions into documents that have similar groupings of these words for quick lookups later. 
Usage Instructions:
Choose the needed output categories in the Settings/Category_Types.ini
Build the needed files in the RQAI.
Manually train the AI via the training method to automatically populate the category types document.

### RQAIDaemon Class
The RQAIDaemon handles the automatic backup of RQAI internal data files to ensure that the data can not only be rolled back, but also that data can be fully restored from past verified points.

#### TODO: 
provide document sorting methods in conjunction with the BST classes. --completed --11/2--
Implement the BST classes to decrease the number of lookups needed as the dataset grows. --completed 11/2--
Change local file accesses during initialization to check data integrity instead of committing to local memory. --completed 11/4--
Multiple OQuestions txt files for separate categories.
Provide a distinction between manual training and AI training. --completed 11/3--
Version control with manual and AI training to allow for corrections and rollbacks with bad data. --completed 11/3--
Multiprocessing daemon to help with backups. --completed 11/8--
Move or delete old data automatically to prevent clutter or buildup.
Give the RQAI full control to expand the dataset given to it as fast as it's able too.
Make Organized Questions the only set of questions that's referenced in automatic question lookup.