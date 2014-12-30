#!/usr/bin/python

import subprocess
import signal
import os
import time
import datetime
import random

import setup
import analyse
import followers

SETUP = True		# If True: Initializes system by switching on monitor mode
shutdown = True		# If True: the pi will shutdown after the no. of loops below
loopLimit = 60		# 1 loop = approx 30sec

loopFrequency = 5	# How often tshark's out put is read (seconds)
previousLines = 2	# Used to compare how many signals are currently in range (must be set to 2 initially)


def formatTime():
	now = datetime.datetime.now()
	currentTime = now.strftime("%H:%M:%S")
	return currentTime

def readData():
# Read tshark's latest output
	file = open("scan.out", "r")
	data = file.read()
	file.close()
	return data.splitlines() # Each line of the file is a different item in this 'data' list

def display(data):
# Display the information collected
# This will eventually have different settings for different hardware (e.g. monitor vs LEDs)
	information = inspect(data)
	os.system("clear")
	print""" 
-------------------------------
          PROXIMITY
-------------------------------"""
	print "Scanning...",
	print """ 
-------------------------------
MAC"""
#Time                        MAC"""
	loopNumber = len(information) -1
	while loopNumber >= 0:
#		individual = information[loopNumber].split()
#		print """ 
#%s      %s""" % (individual[0], individual[1])
		print information[loopNumber]
		loopNumber = loopNumber -1
	print "-------------------------------"
	oldestMatches = analyse.recordData(information) 		# Compare current signals to past MACs in range
	hitCount = followers.count(oldestMatches)
	print "\n %s hits" % hitCount

def inspect(data):
# Put the raw tshark data through all the analysis functions & return useful information
	newData = analyse.checkForNew(data)
	information = analyse.filter(newData)
#	print "New data: %s" % len(information)
	readyData = analyse.removeDuplicate(information)
#	print "Uni data: %s" % len(unique)
#	readyData = addTimestamp(unique)
#	print "Tim data: %s" % len(readyData)
	return readyData

def main():
# Main loop brings all of the functionality together
	print "Initializing..."
	if SETUP == True:
		setup.setup()
	time.sleep(5)
	loopCount = 0
	while True:
		setup.scan()
		data = readData()
		display(data)
		loopCount = loopCount +1
		if loopCount >= loopLimit:
			if shutdown == True:
				followers.shutdownDisplay()
				print "SHUT DOWN!"
				os.system("sudo shutdown -h now")
			else:
				loopCount = 0
if __name__ == '__main__':
	main()
