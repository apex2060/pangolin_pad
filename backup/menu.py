import time
import subprocess
import os
import sys
import Adafruit_CharLCD as LCD

programA = '/home/pi/jam/time/timelapse.py'
programB = '/compile.py'

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

lcd.set_color(1,1,1)

menuArray = ['Run_program', 'Settings', 'IP', 'Exit_menu', 'Shutdown']
lastItem = len(menuArray) -1
topLine = 0
botLine = 1

def menu():
# Scrollable menu
	buttons = ( (LCD.SELECT, 'Select', select ),
	            (LCD.LEFT,   'Left',   null   ),
	            (LCD.UP,     'Up',     up     ),
	            (LCD.DOWN,   'Down',   down   ),
	            (LCD.RIGHT,  'Right',  null   ) )

	try:
	        print 'Press Ctrl-C to quit.'
	        while True:
			
			lcd.message('  %s\n> %s\n' % (menuArray[topLine], menuArray[botLine]))
	                # Loop through each button and check if it is pressed.
	                for button in buttons:
	                        if lcd.is_pressed(button[0]):
					button[2]() # Call the fucntion named in the button list
	                                time.sleep(0.8)
				        lcd.clear()


	except KeyboardInterrupt:
	        lcd.clear()
	        lcd.set_color(0,0,0)

def null():
# Nothing happens when Left or Right are pressed
	pass

def select():
# Run module named in the array
	funcArray[botLine]()

def up():
# Scroll up through items
	global topLine
	global botLine

	topLine = topLine -1
	if topLine <0:
		topLine = lastItem
	botLine = botLine -1
	if botLine <0:
		botLine = lastItem

def down():
# Scroll down through items
	global topLine
	global botLine

	topLine = topLine +1
	if topLine > lastItem:
		topLine = 0
	botLine = botLine +1
	if botLine > lastItem:
		botLine = 0


# --- OPTIONS THAT EXECUTE WHEN SELECTED ---

def program():
	lcd.clear()
	buttons = ( (LCD.SELECT, 'Select'),
	            (LCD.LEFT,   'Left'  ),
	            (LCD.UP,     'Up'    ),
	            (LCD.DOWN,   'Down'  ),
	            (LCD.RIGHT,  'Right' ) )

	selection = 0
	loop = True
	try:
	        print 'Press Ctrl-C to quit.'
	        while loop == True:
			lcd.message('Start Timelapse?\n')
			if selection == 0:
				lcd.message('> Yes   |     No')
			elif selection == 1:
				lcd.message('  Yes   |   > No')

	                # Loop through each button and check if it is pressed.
	                for button in buttons:
	                        if lcd.is_pressed(button[0]):
					if button[1] == 'Left':
						selection = 0
					if button[1] == 'Right':
						selection = 1
					if button[1] == 'Select':
						if selection == 0:
							os.system('sudo python /home/pi/jam/time/timelapse.py')
						else:
							loop = False
	                                time.sleep(0.8)
				        lcd.clear()
	except KeyboardInterrupt:
	        lcd.clear()
	        lcd.set_color(0,0,0)


def settings():
	lcd.clear()
	lcd.message('Change timelapse\nsettings')
	time.sleep(1)
	os.system('sudo python /home/pi/jam/time/setup.py')
	lcd.clear()

def ip():
# Displays current IP address for 5 seconds
	lcd.clear()
        output = subprocess.check_output("sudo hostname -I", shell=True)
        lcd.message('IP: %s' % output)
	
	buttons = ( (LCD.SELECT, 'Select'),
	            (LCD.LEFT,   'Left'  ),
	            (LCD.UP,     'Up'    ),
	            (LCD.DOWN,   'Down'  ),
	            (LCD.RIGHT,  'Right' ) )

	loop = True
	lcd.message('\n> Main menu')
	try:
	        while loop == True:
			time.sleep(0.5)
	                # Loop through each button and check if it is pressed.
	                for button in buttons:
	                        if lcd.is_pressed(button[0]):
					if button[1] == 'Select':
						loop = False
					        lcd.clear()
					time.sleep(0.8)
	except KeyboardInterrupt:
	        lcd.clear()
	        lcd.set_color(0,0,0)
	

        lcd.clear()

def exit():
	lcd.clear()
	buttons = ( (LCD.SELECT, 'Select'),
	            (LCD.LEFT,   'Left'  ),
	            (LCD.UP,     'Up'    ),
	            (LCD.DOWN,   'Down'  ),
	            (LCD.RIGHT,  'Right' ) )

	selection = 0
	loop = True
	try:
	        while loop == True:
			lcd.message('Exit menu?\n')
			if selection == 0:
				lcd.message('> Yes   |     No')
			elif selection == 1:
				lcd.message('  Yes   |   > No')

	                # Loop through each button and check if it is pressed.
	                for button in buttons:
	                        if lcd.is_pressed(button[0]):
					if button[1] == 'Left':
						selection = 0
					if button[1] == 'Right':
						selection = 1
					if button[1] == 'Select':
						if selection == 0:
							lcd.clear()
							lcd.set_color(0,0,0)
							sys.exit()
						else:
							loop = False
	                                time.sleep(0.8)
				        lcd.clear()
	except KeyboardInterrupt:
	        lcd.clear()
	        lcd.set_color(0,0,0)



def shutdown():
	lcd.clear()
	buttons = ( (LCD.SELECT, 'Select'),
	            (LCD.LEFT,   'Left'  ),
	            (LCD.UP,     'Up'    ),
	            (LCD.DOWN,   'Down'  ),
	            (LCD.RIGHT,  'Right' ) )

	selection = 0
	loop = True
	try:
	        while loop == True:
			lcd.message('Shutdown?\n')
			if selection == 0:
				lcd.message('> Yes   |     No')
			elif selection == 1:
				lcd.message('  Yes   |   > No')

	                # Loop through each button and check if it is pressed.
	                for button in buttons:
	                        if lcd.is_pressed(button[0]):
					if button[1] == 'Left':
						selection = 0
					if button[1] == 'Right':
						selection = 1
					if button[1] == 'Select':
						if selection == 0:
							os.system('sudo halt')
						else:
							loop = False
	                                time.sleep(0.8)
				        lcd.clear()
	except KeyboardInterrupt:
	        lcd.clear()
	        lcd.set_color(0,0,0)


	

# List of the above functions
funcArray = [program, settings, ip, exit, shutdown]


if __name__ == '__main__':
	menu()
