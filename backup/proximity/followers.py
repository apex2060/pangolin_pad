import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

def count(oldestMatches):
# Counts how many people have been following for > safe time defined by the no. of lists in analyse.py
	try:
		hitCount = len(oldestMatches)
	except:
		hitCount = 0
	GPIO.output(25,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(25,GPIO.LOW)
	LEDdisplay(hitCount)

	return hitCount

def LEDdisplay(hitCount):
# Displays the no. of followers in range on 5 LEDs + 1 'scanning' LED
	# 'SCANNING' LED ON
	GPIO.output(14,GPIO.LOW)
	GPIO.output(15,GPIO.LOW)
	GPIO.output(18,GPIO.LOW)
	GPIO.output(23,GPIO.LOW)
	GPIO.output(24,GPIO.LOW)

	hitCount = hitCount
	print "LEDs: ",
	if hitCount >= 1:
		#LED 1 ON
		GPIO.output(14,GPIO.HIGH)
		print "1 ",
	if hitCount >= 2:
		# LED 2 ON
		GPIO.output(15,GPIO.HIGH)
		print "2 ",
	if hitCount >= 3:
		# LED 3 ON
		GPIO.output(18,GPIO.HIGH)
		print "3 ",
	if hitCount >= 4:
		# LED 4 ON
		GPIO.output(23,GPIO.HIGH)
		print "4 ",
	if hitCount >= 5:
		#LED 5 ON
		GPIO.output(24,GPIO.HIGH)
		print "5 ",

def shutdownDisplay():
	GPIO.cleanup()	
	GPIO.setup(25,GPIO.OUT)
	x = 5
	while x > 0:
		GPIO.output(25,GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(25,GPIO.LOW)
		time.sleep(0.5)
		x = x-1
def test():
# Passes data to LED function to test GPIO setup
	x = 0
	while x < 7:
		print "\nTest: %s hit\n" % x
		LEDdisplay(x)
		x = x +1
		time.sleep(1)

def testTwo(list):
	count(list)
	time.sleep(3)	
	shutdownDisplay()

if __name__ == "__main__":
	testTwo([1, 2])
#	test()
	GPIO.cleanup()

