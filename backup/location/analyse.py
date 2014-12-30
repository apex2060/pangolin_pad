#!/usr/bin/python

import calculation

def distance(filename):
	loop = 0
	distance = []

	# Read each line from file & save to list
	with open('/home/pi/Programs/location/logs/%s' % filename) as f:
		content = f.readlines()
	
	# Remove \n characters
	content = [x.strip('\n') for x in content]
	
	entries = len(content)
	entries = entries -1
	while entries > 0:
		loc = content[entries]
		loc = loc[13:] # Remove timestamp
		if loc == "Signal Lost" or loc == "Data Error": # Exclude error values
			pass
		else:
	#		print loc
			locStart = loc
			middle = locStart.index('N') + 1
			start = [locStart[:middle], locStart[middle:]]
			decStart = calculation.decimalCoordinates(start[0], start[1])
	#		print decStart
	
		entries = entries - 1
	
		# Repeat for next log
		loc = content[entries]
		loc = loc[13:]
		if loc == "Signal Lost" or loc == "Data Error":
			pass
		else:
	#		print loc
			locEnd = loc
			middle = locEnd.index('N') + 1
			end = [locEnd[:middle], locEnd[middle:]]
			decEnd = calculation.decimalCoordinates(end[0], end[1])
	#		print decEnd
	
		# Calculate distance between each pair of points
		distance.append(float(calculation.haversine(decStart, decEnd)))
	
		# While testing, only loop once 
		#break
	
	# Calculate total distance travelled
	totalKm = sum(distance)
	totalMiles = calculation.convertDistance(totalKm, 'km')
	print "\nDistance travelled:\n%s km\n%s %s" % (totalKm, totalMiles[0], totalMiles[1])
	return totalKm

def calculateCalories(distance, timeTaken, weight):
	distance = float(distance)
	timeTaken = float(timeTaken) / 60
	speed = distance / timeTaken
	calories = calculation.calories(speed, float(weight), timeTaken)
	return calories

if __name__ == "__main__":
	filename = raw_input('File name: ')
	dist = distance(filename)
	timeTaken = raw_input('\nTime taken (minutes): ')
	weight = 70
	calories = calculateCalories(dist, timeTaken, weight)
	print "%s calories burned" % calories
