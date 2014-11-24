#!/usr/bin/python

# -------------------------------------------------------------------------------
# COTSWOLD JAM TIME-LAPSE DEMO
# This is a simple python script that automates the raspistill- & MEncoder-based time-lapse process
# that I brought to the Nov '14 Cotswold Raspberry Jam.

# Read the full tutorial on: www.pangolinpad.wordpress.com/category/cotswold-jam/november-14/
# -------------------------------------------------------------------------------

# Using os is the simplest way I've found of running linux commands in python.
# You'll see it below as os.system('some sort of command'):
import os		

# The following 4 variables can be set to whatever you like:
videoName = 'timelapse'	# The name given to the final video
filename = 'myImage'	# Every time-lapse frame's name will start with this.
interval = 1000		# Time (in milliseconds) between capturing each frame (1 sec = 1,000 millisec)
duration = 1800000	# Time (in milliseconds) that the time-lapse will capture for (1 hr = 360,000 millisec)

delete = True		# If this is set to True, the program will delete all the frames once the video is complete

def capture(interval, duration):
	# This captures the time-lapse frames.

	# You need to pass it two bits of info: the *interval* between shots and the total *duration* you want
	# the timelapse to cover. These are then included in the raspistill command below (filename comes from above):
	os.system('raspistill -o ' + filename + '_%04d.jpg -tl ' + str(interval) + ' -t ' + str(duration))

	# This will return 'True' to let you know when the entire capture is complete:
	return True

def list():
	# Lists all the frames (in order) in a single text file for use by MEncoder
	os.system('ls %s* > stills.txt' % filename)

def mencoder():
	# Runs the MEncoder program that merges all of your stills into a video. I think it work at a pace of roughly 1 frame each second on a Model B.
	os.system('mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o %s.avi -mf type=jpeg:fps=24 mf://@stills.txt' % videoName)
	return True

def main():
	# This is the main bit of the program that runs all of the above in the correct order
	# It also prints helpful messages at each stage of the process or error messages if something goes wrong
	print 'Capturing... \nInterval = %s ms \nDuration = %s ms \n' % (interval, duration)
	if capture(interval,duration) == True:
		print 'Capture complete'
		list()
		print 'Compiling... (this may take some time)\n'
		if mencoder() == True:
			print '\nCompile successful'
			if delete == True:
				print 'Deleting frames...'
				os.system('sudo rm %s*' % filename)
				os.system('sudo rm stills.txt')
			print 'Done!'
		else:
			print 'ERROR: Compile unsuccessful, problem with MEncoder'
	else:
		print 'ERROR: Capture unsuccessful, problem with raspistill'


# Finally, this bit sets off everything contained in the main() section above & starts the program:
main()
