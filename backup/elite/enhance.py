# =======================
# CMDR's LOG ENHANCEMENT
# =======================
# Intended for use with CMDR Dharkamen's trade tool, this program allows multiple
# users to merge their system_data.txt files for collaborative trade route records.
# I feel that online trade tools are a bit too close to cheating, but recording
# supply & demand alone is pretty boring so the ability to share with your friends
# seems to be a good middle ground.
# -----------------------
# v 0.1
# -----------------------

from Tkinter import *   # Used for the GUI interface
import tkMessageBox
import ttk
import os       # Used for loading & saving files
import sys      # For safely exiting the program
#import string   # Used to remove \t characters from imported file
import re

selected_file = "system_data(test).txt"  # Default filepath

# Each GUI window must be stored in a global variable so
# that they can be opened/closed by different functions:
inputWindow = 0 


# ----- FILE OPERATIONS -----
def load_file(filename):
        # Load the system_data.txt file's contents
        loadFile = open(filename, 'r')      # Open file
        contentList = loadFile.readlines()  # Save each line in a contentList
        cleanList = []
        for line in contentList:
                cleanLine = re.sub(r'[\n\t]', '', line) # Remove tabs & newlines
                if cleanLine <> '' and cleanLine <> ' ':
                        cleanList.append(cleanLine)

        return cleanList


def compare_files(filename):
        # Take entered file name & compare it with the original system_data.txt
        global selected_file
        selected_file = filename # Save filename to global variable

        # Retrieve data from the new & old system_data.txt files
        newFile = load_file(selected_file)
        oldFile = load_file("system_data.txt")

        createDict(newFile)

        # Cose the initial Input window
        close_window()


# ----- STRING MANIPULATIONS -----
def createDict(data):
        # Create an easily comparable dictionary from the loaded file data
        systemDict = {} # Create dictionary to hold all data
        data = data[3:] # Remove 1st 3 items ['\xef\xbb\xbf', 'Save Data', '{']

        temp = [] # Temporary list to hold commodity info
        for item in data:
                if item == '}':
                        # End of section, save data to dictionary:
                        try:
                                #           System  :  [StationA, [commodity1, commodity2, ...], ...]
                                systemDict[temp[0]] = temp[2:]

                        except:
                                # Multiple '}' in succession
                                print '}'
                        temp = [] # Clear temporary storage for next section
                else:
                        temp.append(item)

        # DEBUG
        print systemDict.items()

        return systemDict
                        
##### NOTES
## The bit above works if there's only 1 station per system.
## To cope with multiple stations, I need to count the no. of '}', for example:

## System1
## {
## StationA
## {
## [Commodities]
## Notes
## } (1 - End of Notes)
## } (2 - End of StationA)
## StationB
## {
## Commodities etc. etc.
## Notes
## } (1 - End of Notes)
## } (2 - End of StationB)
## } (3 - End of System1)
## System2
## { etc.

# ----- GUI OPERATIONS -----
def close_program():
        inputWindow.destroy()
        sys.exit()

def close_window():
        inputWindow.destroy()

def displayInput():
        # Produce Main GUI window & receive user input (filepath)"
        global inputWindow
        inputWindow = Tk()
        inputWindow.title("CMDRs Log Enhancement")
        
        # Create message
        message = Label(inputWindow,text="""
This program will combine all Commodity data in the supplied file
with your own copy.

Enter the name of the new system_data.txt file below:""", justify=LEFT)
        message.grid(row=0, column=0, columnspan=3) # Apply to window

        # Set up text input
        e = Entry(inputWindow, width=45)
        e.insert(0,selected_file) # Placeholder text
        e.focus_set()   # User can type without needing to click the box first
    
        e.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky=E,) # Apply to grid

        # Create button
        OKbutton = Button(inputWindow,text="OK", width=10, command= lambda: compare_files(e.get()))
        OKbutton.grid(row=1, column=2, padx=2, sticky=W) # Apply to grid

        inputWindow.bind('<Return>', lambda eff: compare_files(e.get())) # Pressing Enter at any point triggers the next step

        inputWindow.mainloop() # Display window



if __name__ == '__main__':
    displayInput()
