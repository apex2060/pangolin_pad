#!/usr/bin/python

# HEADLESS TIMELAPSE
# Intended for use with the LCD screen & associated menu.py script

# This is the simplest way I've found of running linux commands in python.
# You'll see it below as os.system('some sort of command'):
import os		

# Added for demo use, not included in gitHub version
import datetime
import time
import LCD

# The following 4 variables can be set to whatever you like:
videoName = '/home/pi/jam/time/timelapse'	# The name given to the final video
filename = 'myImage'	# Every timelapse frame's name wil start with this.
settingsFile = '/home/pi/jam/time/settings.txt' # Interval & duration stored here
delete = True		# If this is set to True, the program will delete all the frames once the video is complete

def getSettings():
# Load duration & interval settings from file
	settings = open(settingsFile, 'r')
	setList = settings.read()
	setList = setList.splitlines()
	duration = setList[1].split(':')
	duration = duration[1]
	interval = setList[0].split(':')
	interval = interval[1]
	mySettings = [int(interval), int(duration)]
	return mySettings

def capture(interval, duration):
	# This captures the timelapse frames.

	# You need to pass it two bits of info: the *interval* between shots and the total *duration* you want
	# the timelapse to cover. These are then included in the raspistill command below:
	os.system('raspistill -o ' + filename + '_%04d.jpg -tl ' + str(interval) + ' -t ' + str(duration))

	# This will return 'True' to let you know when the entire capture is complete:
	return True

def list():
	# Lists all the frames in a single text file for use by MEncoder
	os.system('ls %s* > stills.txt' % filename)

# Added for demo use, not included in gitHub version:
def getTime():
	now = datetime.datetime.now()
	return now.strftime("%H%M")

def mencoder():
	# Runs the MEncoder program that merges all of your stills into a video
	newName = "%s%s" % (videoName, getTime())

	os.system('mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o %s.avi -mf type=jpeg:fps=24 mf://@stills.txt' % newName)
	return True

def main():
	# This is the main bit of the program that runs all of the above in the correct order
	# It also prints helpful messages at each stage of the process or error messages if something goes wrong
	mySettings = getSettings()
	print 'Capturing... \nInterval = %s ms \nDuration = %s ms \n' % (mySettings[0], mySettings[1])
	LCD.colour([0,1,0])
	LCD.display("TIMELAPSE.PY\nI:%ss D:%ss" % (mySettings[0]/1000, mySettings[1]/1000))

	if capture(mySettings[0], mySettings[1]) == True:
		print 'Capture complete'
		LCD.display("TIMELAPSE.PY\nCompiling video")
		list()
		print 'Compiling... (this may take some time)\n'
		if mencoder() == True:
			print '\nCompile successful'
			LCD.display("TIMELAPSE.PY\nVideo ready")
			time.sleep(1)
			if delete == True:
				print 'Deleting frames...'
				os.system('sudo rm %s*' % filename)
				os.system('sudo rm stills.txt')
			print 'Done!'
			LCD.display("TIMELAPSE.PY\nExit program")
			time.sleep(1)
		else:
			print 'ERROR: Compile unsuccessful, problem with MEncoder'
			LCD.display("TIMELAPSE.PY\nMEncoder error")
	else:
		print 'ERROR: Capture unsuccessful, problem with raspistill'
		LCD.display("TIMELAPSE.PY\nRaspistill error")
	LCD.off()

# Finally, this bit sets off everything contained in the main() section above & starts the program:
main()
#getSettings()
