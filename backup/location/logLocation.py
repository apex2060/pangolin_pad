#!/usr/bin/python

#-----LOG LOCATION-----
# Allows headless logging of location data, may be incorporated
# into larger programs to associate location with other readings
# by simply passing more data to the writeFile() function.

import time
import datetime
import myGPS
import os
import subprocess
import gmail
import calculation

logFile = 0		# This global variable allows many functions to access the .log file
shutdown = False	# By default, the pi will not shut down when logLocation is complete

# Change the settings below:
frequency = 60		# The number of seconds between each poll of the GPS
totalTime = 10800	# The max. length of (seconds) time you want the program to run

def config():
	# Read set-up instructions from log.config file
	configFile = open('/home/pi/Programs/location/log.config', 'r')
	settings = configFile.read()

	SHUTDOWNindex = settings.index("SHUTDOWN")
	SHUTDOWNsetting = SHUTDOWNindex + 9
	if settings[SHUTDOWNsetting] == '1':
		global shutdown
		shutdown = True
	RUNindex = settings.index("RUN")
	RUNsetting = RUNindex + 4
	if settings[RUNsetting] == '1':
		main()
	else:
		print "[logLocation.py]: log.config file must be set to RUN=1 for GPS to run."
	

def initialise():
	# Set the baud rate to match that of the GPS hardware
	subprocess.call('sudo stty -F /dev/ttyUSB0 4800', shell=True)
	FROM = "gmurden22@gmail.com"
	PASSWORD = "youtube2211"
	TO = "gmurden22@hotmail.co.uk"
	SUBJECT = "Pi Current Location"
	MESSAGE = """The B+ GPS module has been started. 
At %s, the starting co-ordinates were:
 %s.""" % (currentTime()[1], getData())
	try:
		gmail.message(FROM,PASSWORD,TO,SUBJECT,MESSAGE)
	except:
		print "Error: Message failed to send"

def currentTime():
	# Format current date/time
	now = datetime.datetime.now()
	date = now.strftime("%d%b")
	time = now.strftime("%H:%M:%S")
	formatTime = [date, time]
	return formatTime

def openFile():
	# Open or create a file for the current date & start the log with a header
	global logFile
	formatTime = currentTime()
	filename = "/home/pi/Programs/location/logs/%s.log" % formatTime[0]
	logFile = open(filename, 'a', 0)
	logFile.write("\n-----Log Started: %s-----" % formatTime[1])
	return filename

def writeFile(data):
	# Appends lines of text to today's file
	global logFile
	print data
	logFile.write("\n> %s" % data)

def getData():
	# Fetch & format data from custom-made GPS module
	locationData = myGPS.read()
	lat = locationData[0]
	long = locationData[1]
	if lat == "S":
		coordinates = ["Data", "Error"]
	elif lat[0] == ",":
		coordinates = ["Signal", "Lost"]
	else:
		latDeg = lat[0:2]
		latMin = lat[2:9]
		latDir = lat[-1]
		lat = "%sdeg %s%s" % (latDeg, latMin, latDir)

		longDeg = long[0:2]
		longMin = long[3:9]
		longDir = long[-1]
		long = "%sdeg %s%s" % (longDeg, longMin, longDir)

		coordinates = [lat, long]
	return coordinates

def analyse(start, end):
	decimalStart = calculation.decimalCoordinates(start[0],start[1])
	decimalEnd = calculation.decimalCoordinates(end[0],end[1])
	distanceTravelled = calculation.haversine(decimalStart, decimalEnd)
	return distanceTravelled

def progressDisplay(status):
	# Visual sign that the program is running. This could be replaced by GPIO LEDs etc.
	if status == 1:
		display = "|"
	if status == 2:
		display = "||"
	if status == 3:
		display = "|||"
	if status == 4:
		display = " ||"
	if status == 5:
		display = "  |"
	if status == 6:
		display = "   "
	return display
	
def main():
	# Display on-screen information at startup & run the programs's main loop
	global totalTime

	formatTime = currentTime()
	header = "----------LOCATION LOGGING-----------"
	timeNote =  "System time at startup: %s" % formatTime[1]
	
	filename = openFile()
	filename = filename[-9:]
	fileNote = "Saving logs to %s\n-------------------------------------" % filename
	footer = "-------------------------------------"

	# Main loop:
	try:
		initialise()
		count = 1
		while True:
	# Try to capture the first and last good locations from the GPS so they cab be
	# passed to the new analyse() function and appended to the end of the journey file.
			os.system('clear')
			print header
			print timeNote
			print fileNote
			if count == 7:
				count = 1
			display = progressDisplay(count)
			print "	%s	%s	%s" % (display, display, display)
			print footer
			formatTime = currentTime()
			formatTime = formatTime[1]
			locData = getData()
			data = "%s : %s %s" % (formatTime, locData[0], locData[1])
			writeFile(data)
			time.sleep(frequency)
			totalTime = totalTime - frequency
			count = count + 1
			
			if totalTime < 0:
				writeFile("\n\n")
				if shutdown == True:
					os.system('sudo shutdown -h now')
				break

	except KeyboardInterrupt:
		# When the program is stopped, a final line is added to the log file.
		# This will help distinguish between journeys if more than one is made in one day
		writeFile("\n\n")
		print "Logging stopped"

if __name__ == "__main__":
	config()
