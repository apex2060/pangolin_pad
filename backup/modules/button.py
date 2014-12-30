#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import os

# GPIO pin button is connected to:

filename = "/home/pi/Programs/modules/button.config"
buttonPin = 4
LEDpin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setup(buttonPin,GPIO.IN)
GPIO.setup(LEDpin,GPIO.OUT)

def buttonEvent(buttonPin):
# What happens when button is pressed:
	GPIO.output(LEDpin,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(LEDpin,GPIO.LOW)
	print "Starting Program..."

	os.system('sudo nohup python /home/pi/Programs/wifi/proximity/main.py &')

def checkFile(filename):
	file = open(filename, 'r')
	content = file.read()
	try:
		content = int(content)
		if int(content) == 1:
			return True
		else:
			return False
	except:
		return False

def main():
	if checkFile(filename) == True:
		print "/home/pi/Programs/modules/button.py is running, change %s to '0' to prevent this" % filename
		# Flash LED to indicate readyness
		x = 3
		while x > 0:
			time.sleep(0.5)
			GPIO.output(LEDpin,GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(LEDpin,GPIO.LOW)
			x = x-1
	
		# Program sleeps until button is pressed:
		GPIO.wait_for_edge(buttonPin,GPIO.RISING)
		buttonEvent(buttonPin)
	
		GPIO.cleanup()

	else:
		print "/home/pi/Programs/modules/button.py will not run as %s <> 1" % filename

if __name__ == "__main__":
	main()
