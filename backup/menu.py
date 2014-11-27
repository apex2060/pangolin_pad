#!usr/bin/python

import os
import sys
import time
import subprocess
import Adafruit_CharLCD as LCD

programA = '/home/pi/jam/time/timelapse.py'
programB = '/home/pi/Programs/LCD/blank.py'

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
# Headless run program functionality
	localButtons = ( (LCD.SELECT, 'Back' ),
	            (LCD.LEFT,   'RUN' ),
	            (LCD.UP,     'Back' ),
	            (LCD.DOWN,   'Back' ),
	            (LCD.RIGHT,  'Cancel' ) )


# Runs the specified program
	name = program.split('/')
	lcd.clear()
	lcd.message('%s' % name[-1])

	lcd.message('\n< RUN | CANCEL >')
	loop = True
	while loop == True:
	        # Loop through each button and check if it is pressed.
	        for button in localButtons:
	                if lcd.is_pressed(button[0]):
	                        # Button is pressed, change the message and start program.
	                        lcd.clear()
				time.sleep(0.5)	
				if button[1] == 'RUN':
					lcd.clear()
					lcd.message('Running:\n%s' % name)
					os.system('sudo python %s' % program)
					lcd.clear()
					lcd.message('Running:\nDone!')
					time.sleep(2)

				loop = False
	

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

def info(delay):
	for button in buttons:
		direction = button[0]
		if direction == 0:
			direction = 'Select'
		elif direction == 4:
			direction = 'Left'
		elif direction == 3:
			direction = 'Up'
		elif direction == 2:
			direction = 'Down'
		else:
			direction = 'Right'

		funct = button[1][1:]
		if funct == "Run program":
			funct = button[3].split('/')
			funct = funct[-1]
		lcd.message('%s:\n%s' % (direction, funct))
		time.sleep(delay)
		lcd.clear()
	lcd.message('HEADLESS MENU')

# Make list of button value, text, and associated action.
	     # button    display          command    parameter
buttons = ( (LCD.SELECT, '\nQuit'        , quit    , 0),
            (LCD.LEFT,   '\nIP Address'  , myIP    , 5),
            (LCD.UP,     '\nRun program' , run     , programA),
            (LCD.DOWN,   '\nRun program' , run     , programB),
            (LCD.RIGHT,  '\nInfo'        , info    , 2 ) )

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
