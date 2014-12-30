#!/usr/bin/python

import os
import time
import random

import analyse

def setup():
# Initialise the program by putting the WiFi in monitor mode
	os.system("sudo airmon-ng start wlan0")
	return True

def scan():
# Run tshark in the background, saving output to nohup.out
	randTime = random.randint(12,21) # Irregular wait times in case accidental sync with nearby signals mean we miss them
	print randTime
	os.system("sudo tshark -i mon0 -a duration:%s subtype probereq > scan.out &" % randTime)
	time.sleep(randTime)
	return True

