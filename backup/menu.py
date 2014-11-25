#!usr/bin/python

import os
import sys
import time
import subprocess
import Adafruit_CharLCD as LCD

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

def quit(nill):
# Headless program-exit functionality
	localButtons = ( (LCD.SELECT, 'Back' ),
	            (LCD.LEFT,   'QUIT' ),
	            (LCD.UP,     'Back' ),
	            (LCD.DOWN,   'Back' ),
	            (LCD.RIGHT,  'SHUTDOWN' ) )

	lcd.message('< QUIT\n      SHUTDOWN >')
	loop = True
	while loop == True:
	        # Loop through each button and check if it is pressed.
	        for button in localButtons:
	                if lcd.is_pressed(button[0]):
	                        # Button is pressed, change the message and backlight.
	                        lcd.clear()
				time.sleep(0.5)	
				if button[1] == 'QUIT':
					lcd.clear()
					lcd.set_color(0,0,0)
					sys.exit()
				elif button[1] == 'SHUTDOWN':
					os.system('sudo halt')
					lcd.message('Shutting down...')
					lcd.clear()
					lcd.set_color(0,0,0)
				else:
					loop = False
	lcd.clear()
	lcd.message('HEADLESS MENU')

def myIP(delay):
# Displays current IP address for 5 seconds
	output = subprocess.check_output("sudo hostname -I", shell=True)
	lcd.message(output)
	for n in range(delay +1):
		x = delay - n
		lcd.message('\n%s' % x)
		time.sleep(1)

	lcd.clear()
	lcd.message('HEADLESS MENU')

def run(program):
# Runs the specified program
	name = program.split('/')
	lcd.clear()
	lcd.message('Running:\n%s' % name[-1])
	os.system('sudo python %s' % program)
	lcd.clear()
	lcd.message('Running:\nDone!')
	time.sleep(2)

	lcd.clear()
	lcd.set_color(1,1,1)
	lcd.message('HEADLESS MENU')


def blank(delay):
	for n in range(delay +1):
		x = delay - n
		lcd.message('HEADLESS MENU\nEmpty slot     %s' % x)
		time.sleep(1)

	lcd.clear()
	lcd.message('HEADLESS MENU')

# Make list of button value, text, and associated action.
	     # button    display          command    parameter
buttons = ( (LCD.SELECT, '\nQuit'        , quit    , 0),
            (LCD.LEFT,   '\nIP Address'  , myIP    , 5),
            (LCD.UP,     '\nTime-lapse'  , run     , '/home/pi/jam/time/timelapse.py'),
            (LCD.DOWN,   '\nEmpty slot'  , blank   , 3 ),
            (LCD.RIGHT,  '\nEmpty slot'  , blank   , 3 ) )

try:
	print 'Press Ctrl-C to quit.'
	lcd.message('HEADLESS MENU')
	while True:
	        # Loop through each button and check if it is pressed.
	        for button in buttons:
	                if lcd.is_pressed(button[0]):
	                        # Button is pressed, change the message and backlight.
	                        lcd.message(button[1])
				time.sleep(0.8)
	                        lcd.clear()
				button[2](button[3]) # Calls the function named in button list

except KeyboardInterrupt:
	lcd.clear()
	lcd.set_color(0,0,0)
