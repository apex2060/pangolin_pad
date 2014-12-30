#!/usr/bin/python

import time
import datetime

previousLines = 2	# Used to compare how many signals are currently in range (must be set to 2 initially)

listA = []
listB = []
listC = []
listD = []

def formatTime():
	now = datetime.datetime.now()
	currentTime = now.strftime("%H:%M:%S")
	return currentTime

def checkForNew(data):
# Checks if new signals have been detected & returns only the new ones (those currently in range)
	global previousLines
	lines = len(data)
	if lines > previousLines:
		firstNewSignal = previousLines-2

#		print "Current lines:   %s" % lines
#		print "Previous lines:  %s" % previousLines
#		print "1st New signal:  %s" % firstNewSignal

		previousLines = lines
		newData = data[firstNewSignal:] # Returns all newly detected signals
	else:
		newData = data # Need to change this to output something meanifngful if no signals are in range
	return newData

def filter(data):
# Filter the useful information (MAC address & time) from the rest of the data
	information = []
	loopNumber = len(data) -1
	while loopNumber >= 0:
		try:
			signal = data[loopNumber].split() # Each word in an item from the 'data' list is a different item in this 'signal' list
			information.append(signal[1])
			loopNumber = loopNumber - 1
		except:
			information = "NoNewSignals"
	return information

def removeDuplicate(data):
# When given a list of strings, this returns the list with any duplicate MAC addresses removed
	# Code from peterbe.com/plog/uniqifiers-benchmark works but doesn't preserve the list order
	keys = {}
	for e in data:
		keys[e] = 1
	unique = keys.keys()
	return unique

def addTimestamp(data):
# Works through list of MAC addresses & puts them in a new list alongside the current time
	readyData = []
	loopNumber = len(data) -1
	while loopNumber >= 0:
		readyData.append("%s" % data[loopNumber])
		loopNumber = loopNumber -1
	return readyData


def recordData(readyData):
# Stores 'readyData' list of in-range MAC addresses & times from each loop
	global listA
	global listB
	global listC
	global listD		
	
	listD = listC
	listC = listB
	listB = listA
	listA = readyData

	oldestMatches = compareLists(listA)
	return oldestMatches

def compareLists(currentList):
# Compare current addresses in range with those recorded in the previous loops
# Prints matches from each loop for debugging but only returns the oldest

	oldestMatches = currentList #Uncomment to return matches from current signals

	print '30s ago:'
	list30 = []
	pastList = listB
	for n in currentList:
		match = any(n in e for e in pastList)
		list30.append("%s" %(n if match else " "))

	matches = []
	loopNumber = len(list30) -1
	while loopNumber >= 0:
		if list30[loopNumber] <> " ":
			matches.append("%s" % list30[loopNumber])
		loopNumber = loopNumber -1
	print matches
#	oldestMatches = matches #Uncomment to return matches from 30s ago


	print '60s ago:'
	list60 = []
	pastList = listC
	for n in currentList:
		match = any(n in e for e in pastList)
		list60.append("%s" %(n if match else " "))

	matches = []
	loopNumber = len(list60) -1
	while loopNumber >= 0:
		if list60[loopNumber] <> " ":
			matches.append("%s" % list60[loopNumber])
		loopNumber = loopNumber -1
	print matches
#	oldestMatches = matches #Uncomment to return matches from 60s ago


	print '90s ago:'
	list90 = []
	pastList = listD
	for n in currentList:
		match = any(n in e for e in pastList)
		list90.append("%s" %(n if match else " "))

	matches = []
	loopNumber = len(list90) -1
	while loopNumber >= 0:
		if list90[loopNumber] <> " ":
			matches.append("%s" % list90[loopNumber])
		loopNumber = loopNumber -1
	print matches

#	oldestMatches = matches #Uncomment to return matches from 90s ago
	return oldestMatches
