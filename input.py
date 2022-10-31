import tkinter as tk
from tkinter import simpledialog
 
# Define the root window
ROOT = tk.Tk()
 
# Define input dialog
ROOT.withdraw()
 
# Define the input dialog
USER_INP = simpledialog.askstring(title="Input Test",
                                  prompt="Type your Name?:")
 
# Print the user input
print("Hello", USER_INP)