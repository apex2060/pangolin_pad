#!\usr\bin\python

#-----CUSTOM-MADE GPS PROGRAM-----
# GPSd wouldn't work with my hardware, so I've made this to parse the raw serial data

import os
import subprocess
import time

def read():
	# Reads data from GPS module
	output = subprocess.Popen(["timeout", "1", "sudo", "cat", "/dev/ttyUSB0"], stdout=subprocess.PIPE)
	out, err = output.communicate() 
	location = filter(out)
	return location

def filter(rawData):
	# Filters out the extra data and returns the Lat & Long.
	success = False
	attempt = 1
	while attempt < 11:
#		print "Signal lost %s second(s) ago..." % attempt
		if "GPGGA" in rawData:
			success = True
			index = rawData.index("GPGGA")
			try:
				indexStart = index + 13
				indexStop = indexStart + 29
				coordString = rawData[indexStart:indexStop]
				break
			except:
				success = False
		success = False
		attempt = attempt + 1
		time.sleep(1)

	if success == True:
		data = format(coordString)
		return data
	else:
#		print "Ensure you have run 'screen /dev/ttyUSB0 4800' before running this program"
		return "Searching for satellites..."

def format(coordString):
	# Converts the single string of filtered data to a list of useful figures
	latitude = coordString[0:9]
	longitude = coordString[13:22]
	satellites = coordString[27:29]
	data = [latitude, longitude, satellites]
	return data

def display(runCount):
	# Creates a more visually appealing display format for the GPS data
	if runCount == 1:
		header = """ 
----------------------------------
            myGPS
----------------------------------"""

		status = "\nConnecting, please wait..."
	else:
		locationString = read()
		signal = locationString[2]
		header = """ 
----------------------------------
            myGPS	       %s
----------------------------------""" % signal

		status = """ 
Latitude	Longitude
%s	%s""" % (locationString[0], locationString[1])

	footer = """ 
---------------------------------
(Ctrl + C to exit)
---------------------------------"""
	os.system('clear')
	print header
	print status
	print footer	


def main():
	display(1)
#	rawData = read()
#	print rawData
#	print filter(rawData)
	try:
		while True:
			display(0)
			time.sleep(5)
	except KeyboardInterrupt:
		print "Shutting down..."

if __name__== "__main__":
	main()
