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
                if cleanLine <> '' and cleanLine <> ' ': # Excluse empty list items
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
        data = data[3:] # Remove 1st 3 items ['\xef\xbb\xbf', 'Save Data', '{']

        temp = [] # Temporary list to hold commodity info
        comparisonDict = {} # Final dictionary of info
        lastSystem = data[0] # Used to store the name of the last recorded system (initially the 1st item in the data list)
        countLoop = -1 # Used to count the no. of loops
        countBracket = 0 # Used to count the no. of closing brackets (})
        for item in data:
                countLoop = countLoop +1
                if item == '}':
                        countBracket = countBracket +1

                        if countBracket == 1: # End of station notes
                                if lastSystem in temp: temp.remove(lastSystem) # We don't need the system in the key & the item
                                # Dictionary keyts must eb unique, so if a system has multiple stations, save all to singe System key:
                                if lastSystem in comparisonDict:
                                        comparisonDict[lastSystem] = [comparisonDict[lastSystem], temp] # Retains original commodity data & adds the new
                                else:
                                        comparisonDict[lastSystem] = temp # Save section data into dictionary
                                temp = [] # Empty temporary storage

                        elif countBracket == 2: # End of station
                                lastSystem = compare[countLoop][0] ## THIS NEEDS FIXING

                        elif countBracket == 3: # End of system
                                countBracket = 0
                else:
                        temp.append(item)

        return comparisonDict
                        
# #### NOTES ####
# 
# 
# #### ----- ####

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
