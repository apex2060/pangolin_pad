#import gmail
import outlook
import pgoHeatmap
import os

def getAlertList():
	alertFile = open("alertList.txt", "r")
	alertList = alertFile.readlines()
	numList = []
	for num in alertList:
		numList.append( int(num.rstrip()) )
	alertFile.close()
	return numList

def alert(num, name, lat, lon, expiresAt):
	"Send a notification if a pokemon on the 'interestring' list appears"
	if num in getAlertList():
		mapfile = pgoHeatmap.makeMap(name, lat, lon)
		mapfile = "{0}\\{1}".format(os.path.dirname(os.path.realpath(__file__)), mapfile)
		message =  """ 
A wild {0} appeared!
Location: \t https://www.google.com/maps/preview/@{1},{2},16z 
Expires at:\t{3}""".format(name, lat, lon, expiresAt)
		print "Sending {0}".format(mapfile)
		outlook.sendMessage("RECIPIENT", "PKMN", message, mapfile)


