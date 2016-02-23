#!/usr/bin/python


# FACE DETECTION
# -----------------------
# Graphical version - Will only work from the desktop (enter command 'startx')
# -----------------------
# Simple face detection for the camera module using SimpleCV.
# This will continuously capture images and search them for human features. Which features can be set
# under 'detect()' below.
# As an output, the latest frame will be displayed on-screen with each feature highlighted by a green square.
#------------------------

print "\n Initializing, please wait..."
import subprocess
from SimpleCV import *

def captureImage(height, width, filename):
	# Note: smaller images speed up processing but limit useful range
	# (200x200 range is ~3m & processes 1 frame every ~5 sec)
	# -cfx 128:128 makes the image greyscale, I'm not sure if this affects fps but range remains unchanges
	print "Capturing image"
	subprocess.call("raspistill -t 1 -cfx 128:128 -n -h %s -w %s -o %s" % (height, width, filename), shell=True)
	img = Image(filename)
	return img

def detect(img):
	# Detects all faces in an image (tested with up to 3)
	print "Searching for faces..."
	face = HaarCascade("face.xml") # Change to 'upper_body.xml' or 'eye.xml' to detect other features
	faces = img.findHaarFeatures(face)
	return faces

def draw(f, img):
	# Draws a rectangle over every face ('f') in the image ('img')
	print "Face at " + str(f.coordinates())
	# Overlay image with a layer on which to draw
	facelayer = DrawingLayer((img.width, img.height))
	# Set dimentions of each box
	facebox_dim = (50,50)
	# Centre each box on the detected face's coordinates
	centre_point = (f.coordinates())
	# Build the box with the above details
	facebox = facelayer.centeredRectangle(centre_point, facebox_dim, color=Color.GREEN)
	return facelayer 

def main():
	# Captures an image from the camera module, displays it on-screen and highlights any people
	# by drawing a green square around their face/upper body
	disp = Display()
	height = 200
	width = 200
	filename = "image.bmp"
	while disp.isNotDone():
		try:
			img = captureImage(height, width, filename)
			faces = detect(img) # chnage to detect(img) to focus on faces (better for close-up)
			if faces is not None:
				for f in faces:
					facelayer = draw(f, img)
					# The following line adds the rectangle made by draw() to the image's drawing layer
					img.addDrawingLayer(facelayer)
		
			# This adds the drawing layer over the top of the image
			img.applyLayers()
			# Display the image & its layers on screen
			img.show()
			if disp.mouseLeft:
				break
		except KeyboardInterrupt:
			print "\nProgram Exit"
			break


if __name__ == "__main__":
	main()
