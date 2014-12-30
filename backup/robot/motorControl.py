#!/usr/bin/python

import os
import sys
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motorA = 4
motorB = 7
motorC = 8
motorD = 18

GPIO.setup(motorA, GPIO.OUT)
GPIO.setup(motorB, GPIO.OUT)
GPIO.setup(motorC, GPIO.OUT)
GPIO.setup(motorD, GPIO.OUT)

GPIO.output(motorA, GPIO.LOW)
GPIO.output(motorB, GPIO.LOW)
GPIO.output(motorC, GPIO.LOW)
GPIO.output(motorD, GPIO.LOW)

loop = True

while loop == True:
	os.system("clear")
	print """ 
Motor	pin no.
A	4
B	7
C	8
D	18

Enter motor letter to test, 'Q' to quit."""
	select = raw_input("\n> ")
	select = select.upper()
	
	if select == "A":
		print "Motor A"
		GPIO.output(motorA, GPIO.HIGH)
		GPIO.output(motorB, GPIO.LOW)
		time.sleep(2)
		GPIO.output(motorB, GPIO.LOW)
		GPIO.output(motorA, GPIO.LOW)
		time.sleep(0.5)
	elif select == "B":
		print "Motor B"
		GPIO.output(motorB, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(motorB, GPIO.LOW)
		time.sleep(0.5)
	elif select == "C":
		print "Motor C"
		GPIO.output(motorC, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(motorC, GPIO.LOW)
		time.sleep(0.5)
	elif select == "D":
		print "Motor D"
		GPIO.output(motorD, GPIO.HIGH)
		time.sleep(2)
		GPIO.output(motorD, GPIO.LOW)
		time.sleep(0.5)
	elif select == "Q":
		print "Closing down..."
		GPIO.cleanup()
		sys.exit()
	else:
		print "Invalid selection, please enter A, B, C or D. Type Q to quit."
