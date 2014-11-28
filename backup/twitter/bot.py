##!/usr/bin/python
# TWITTER AD BOT - TEST VERSION
# ==============
# Designed as a free alternative to twitter's advert feature, this program
# scans twitter for key words and replies to all tweets with preset messages.
# --------------
import twitter
import time
import os

DEBUG = True	# Console outputs will appear if set to True
interval = 1	# Time between twitter scans (minutes)

account = 'puzzleIsland'	# API details stored in file with this name
keyfile = 'key_words.txt'	# Search terms stored in file with this name
postHistory = 'postHistory.log'	# This program's posts recorded in file with this name
messageFile = 'messages.txt'	# Your responses are retrieved from here

# Default search terms & messages if none are set in keyFile or messageFile above
defaultSearch = ['keyphrase01', 'keyphrase02']
message00 = "We noticed you tweeted about %s and thought you might be interested in [url]" % defaultSearch[0]
message01 = "Hello. We just saw your tweet about %s, why not take a look at [url]?" % defaultSearch[1]
defaultMessage = [message00, message01]

# -----------------------------------------------------------------------------------------
# THE LINK WITH THE API IS SET UP AND MAINTAINED BY THIS BIT
def newFile():
# Checks id there's an API file present & creates one if not
	# API details
	Ckey = ' '
	Csec = ' '
	Atok = ' '
	Asec = ' '
	if os.path.exists(account + '.dat'):
		if DEBUG:
			print 'DEBUG: API details found'
		return True
	else:
		if DEBUG:
			print 'DEBUG: API details added'
		twitter.new_account(account, Ckey, Csec, Atok, Asec)
	return False

# -------------------------------------------------------------------------------------
# THESE BITS ARE ALL ABOUT SETTING THE KEYWORDS & THE MESSAGES WE WANT TO SEND IN RESPONSE
def readKeywords():
# Read the key words and phrases from the keyword file
	if os.path.exists(keyfile):
		# Read keywords
		if DEBUG:
				print 'DEBUG: Loading keywords'
		readFile = open(keyfile, 'r', 0)
		keywords = readFile.read()
		readFile.close()

		keywords = keywords.split('\n')
		 # Reading from a file adds an empty line, which we don't want in the list
		keywords.pop()
		return keywords
	else:
		# Create file with default keywords
		if DEBUG:
			print 'DEBUG: Using default keywords'
		newFile = open(keyfile, 'w', 0)
		for phrase in defaultSearch:
			newFile.write('%s\n' % phrase)
		newFile.close()
		return defaultSearch

def readMessage():
# Reads preset tweets from message.txt
	if os.path.exists(messageFile):
		# Read messages
		if DEBUG:
			print 'DEBUG: Loading messages'
		readFile = open(messageFile, 'r', 0)
		messages = readFile.read()
		readFile.close()

		messageList = messages.split('\n')
		return messageList
	else:
		# No preset messages, create file with defaults
		if DEBUG:
			print 'DEBUG: Using default messages'
		newFile = open(messageFile, 'w', 0)
		for message in defaultMessage:
			newFile.write('%s\n' % message)
		newFile.close()
		return defaultMessage

def matchPosts():
# Matches keywords with messages so the correct reposne can be posted to each tweet found
	if DEBUG:
		print 'DEBUG: Creating dictionary of responses'
	keywords = readKeywords()
	messages = readMessage()
	postDictionary = {}
	for x in range(len(keywords)):
		postDictionary[keywords[x]] = messages[x]
		if DEBUG:
			print postDictionary[keywords[x]]
#	postDictionary = {
#			'key1': 'value1',
#			'key2': 'value2'
#			}
	return postDictionary

# ---------------------------------------------------------------------------------------
# THESE BITS ACTUALLY INTERRACT WITH TWITTER
def scanOLD():
	# Scan for tweets containing the keywords
	keywords = readKeywords()
	hits = []
	print 'Scanning...'
	for word in keywords:
		try:
			print 'Keyword %s' % word
			hits.append(twitter.read_tweet(account, word))
		except:
			print'E1'

	print '%s tweets found' % len(hits)
	return hits

def scan():
	postDictionary = matchPosts()
	hits = []
	if DEBUG:
		print 'DEBUG: Searching Twitter'
	for keyword, message in postDictionary.items():
		if DEBUG:
			print keyword, message
		# Search for tweets containing the keyword
		hits.append(twitter.read_tweet(account, keyword)) 
		for hit in hits:
			# Pass our response message to respond()
			respond(hit, message) 
	return hits

def respond(tweet, message):
# Posts *message* to the owner of *tweet*
#	print '***%s' % tweet
	if tweet != []:
		data = extract(tweet)
		name = data[0]
		text = data[1]

		myPost = "%s %s" % (name, message)
		if DEBUG:
			print 'DEBUG: Composing response'
	
		if record(name, text, myPost) == True:
			post(myPost)
			print 'POST PLACEHOLDER'
		else:
			if DEBUG:
				print 'DEBUG: %s has been contacted before, ignoring their tweet:\n %s' % (name, text)
				print

	else:
		print 'No hits'

def extract(tweet):
# Extract useful data from tweet dictionary
	dictionary = tweet[0]
	text = dictionary['text']
	userPortion = dictionary['user'] # User details are in a sub-dictionary named 'user'
	name = userPortion['screen_name']
	return (name, text)

def post(message):
# Post preset tweet online
	if DEBUG:
		print 'DEBUG: Sending:\n%s' % message
	twitter.tweet_function(account, message)

# ----------------------------------------------------------------------------------------
# THIS RECORDS ALL OF OUR TWEETS TO PREVENT SPAM & FOR ANALYTICS
def record(customer, theirPost, myPost):
# Makes a note of each tweet caught & what was sent in return 
# RETURNS True IF THIS CUSTOMER HASN'T BEEN CONTACTED BEFORE
	if os.path.exists(postHistory):
		# Read all post history
		if DEBUG:
			print 'DEBUG: Loading post history'
		historyFile = open(postHistory, 'r', 0)
		history = historyFile.read()
		historyFile.close()
		history = history.split('\n')
		if customer in history:
			if DEBUG:
				print 'DEBUG: %s found in post history' % customer
			# We've tweeted at this customer before, ignore their tweet
			return False
		else:
			# Never contacted this customer before, so save their details
			historyFile = open(postHistory, 'a', 0)
			historyFile.write('%s|%s|%s\n' % (customer, theirPost, myPost))
			historyFile.close()	
			if DEBUG:
				print "DEBUG: Added record of %s's tweet to post history" % customer			
			return True
	else:
		# No history file so create a new one with this first tweet included
		if DEBUG:
			print 'DEBUG: Creating post history log'
		newFile = open(postHistory, 'w', 0)
		newFile.write('%s|%s|%s\n' % (customer, theirPost, myPost))
		newFile.close()
		if DEBUG:
				print "DEBUG: Added record of %s's tweet to post history" % customer
		# No history log so we know we've never tweeted to this customer before
		return True


# ----------------------------------------------------------------------------------------
# THIS IS THE MAIN LOOP OF THE PROGRAM THAT BRINGS ALL OF THE ABOVE TOGETHER
def main():
	print 'TWEETBOT is running'
	if DEBUG:
		print 'DEBUG MODE ON'
	print '-------------------'
	print '%s  |  %sm' % (account, interval)
	print '-------------------'
	newFile()
	matchPosts()

	while True:
		hits = scan()
		if hits[0] != []:
			for hit in hits:
				print "%s\n%s\n" % (hit['screen_ name'], hit['text'])
		time.sleep(interval*60)
			
if __name__ == '__main__':
	main()
