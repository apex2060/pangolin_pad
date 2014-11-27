##!/usr/bin/python

# TWITTER AD BOT - TEST VERSION
# ==============
# Designed as a free alternative to twitter's advert feature, this program
# scans twitter for key words and replies to all tweets with preset messages.
# --------------

import twitter
import time
import os

interval = 1			# Time between twitter scans (minutes)
account = 'puzzleIsland'
keyfile = 'key_words.txt'

def newFile():
	# Checks id there's an API file present & creates one if not

	# 22rPi API details
	Ckey = '5jVDB0sTUntE1jYDi8ADUdmIG'
	Csec = 'UA7Gu7H082KS945aODxTeG2XcgPvHzQcqYdRKi5vhS8OzbPgy1'
	Atok = '2535779829-UORPwp6LAtrSSNg3XbJJZ1NX4AdGRA6jxiQAAeF'
	Asec = '4KSNu5E4PPnp5RItux6J8rs5g5vved0trNWEvjPAFabtQ'

	if os.path.exists(account + '.dat'):
		return True
	else:
		twitter.new_account(account, Ckey, Csec, Atok, Asec)
		return True

def readKeywords():
	if os.path.exists(keyfile):
		# Read keywords
		print 'Loading keywords'
		readFile = open(keyfile, 'r', 0)
		keywords = readFile.read()
		readFile.close()
		return keywords

	else:
		# Create file with placeholder keywords
		placeholder = ['keyphrase01', 'keyphrase02']

		newFile = open(keyfile, 'w', 0)
		newFile.write(placeholder)
		newFile.close()		

def post(message):
	print message
	twitter.tweet_function(account, message)

def scan():
	# Scan for tweets containing the keywords
	keyword = readKeywords()
	keyword = keyword.split('\n')
	
	hits = []
	print 'Scanning...'
	for word in keyword:
		try:
			print 'Keyword %s' % word
			hits.append(twitter.read_tweet(account, word))
		except:
			print
	print '%s tweets found' % len(hits)
	return hits
	
def main():
	if newFile() == True:
		print 'API found'
	else:
		print 'API details added'

	while True:
		hits = scan()
		for hit in hits:
			print "%s\n\n" % (hit[0]['screen_ name'], hit[0]['text'])
#		print hits[0][0]
		time.sleep(interval*60)

#	post('uNiTEsTWE220911')

if __name__ == '__main__':
	main()
