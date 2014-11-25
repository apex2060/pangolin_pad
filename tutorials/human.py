# FACE DETECTION
# --------------------
# Command line version
# --------------------
# Simple face-detecting script for the camera module using SimpleCV.
# This will continuously take images and search them for himan features. Which features can 
# be set on the line 'faces = img.findHaarFeatures('face.xml').
# As an out put it will print the coordinates for each face detected.
#--------------------- 

print 'Initialize'	# SimpleCV is BIG so it takes a good 5 seconds to import
from SimpleCV import Display, Image
import os			

filename = 'frame'	# Save each loop's image under the same name so it's overwritten

try:
	print 'Press Ctrl+C to exit.'
	while True:
		# Take an image using raspistill. The small resolution helps speed things up
		print 'Capturing...'
		os.system('raspistill -n -w 500 -h 500 -o %s.jpg' % filename)
		img = Image('%s.jpg' % filename)	# Pass the captured image to SimpleCV

		print 'Searching...'
		# This is the bit that does all the work:
		# Try putting 'upper_body.xml' or 'eye.xml' in place of 'face.xml'
		faces = img.findHaarFeatures('face.xml') 

		if faces != []: # If any faces are found
			print 'Face(s) found at:'
			for face in faces:
				# Print the coordinates for each face found
				coOrd = face.coordinates()
				print '%s' % coOrd
		else:
			print 'No faces found.'
		print '--------------------'	# This just breaks things up for easy viewing

except KeyboardInterrupt:
	print 'Exit'

