#!/usr/bin/python

#----TWITTER MODULE----
#Allows other programs to  tweet without needing to re-enter the keys below

#v 1.0

# Import thiis file to main program E.G:
# import twitter

# Save your information to a variable named 'tweet'
# and if desired, an image's file name to 'image'
# Call this function to post the infromation to twitter.
# The API details must be pre-saved in a .dat file specified 
# by the account parameter when thefunction is called. E.G:
# twitter.tweet_function(account, tweet)

#-------------------

from twython import Twython # Twitter API interface
import pickle # To load API keys from file

def read_tweet(account, keyword):
# Reads latest post from the specified user and
# returns the text in a variable. Originally designed
# as a means for a program to receive instructions remotely.
	fileName = account + ".dat"

	load_file = open(fileName,'rb')
	load_data = pickle.load(load_file)
	load_file.close()	

	#consumer keys relate to the app, access keys to the account
	CONSUMER_KEY = load_data['itemOne']
	CONSUMER_SECRET = load_data['itemTwo']
	ACCESS_KEY = load_data['itemThree']
	ACCESS_SECRET = load_data['itemFour']

	#save above details to single variable
	api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

	search = api.search(q = keyword)
	tweets = search['statuses']

	return tweets

def tweet_function(account, tweet):
# Posts a tweet to a twitter account associated with pre-recorded
# API details. The location of these details is provided by the
# account parameter
	fileName = account + ".dat"

	load_file = open(fileName,'rb')
	load_data = pickle.load(load_file)
	load_file.close()	

	#consumer keys relate to the app, access keys to the account
	CONSUMER_KEY = load_data['itemOne']
	CONSUMER_SECRET = load_data['itemTwo']
	ACCESS_KEY = load_data['itemThree']
	ACCESS_SECRET = load_data['itemFour']

	#save above details to single variable
	api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
	
	#post tweet contained in the tweet parameter
	api.update_status(status=tweet)

def tweet_image(account, tweet, image):
# Tweet an image to a twitter account associated with pre-recorded
# API details. The location of these details is provided by the
# account parameter. The image must be within the current directory
# and saved as a .jpg

	fileName = account + ".dat"

	load_file = open(fileName,'rb')
	load_data = pickle.load(load_file)
	load_file.close()	

	#load image
	image = image + '.jpg'
	i = open(image,'rb')

	#consumer keys relate to the app, access keys to the account
	CONSUMER_KEY = load_data['itemOne']
	CONSUMER_SECRET = load_data['itemTwo']
	ACCESS_KEY = load_data['itemThree']
	ACCESS_SECRET = load_data['itemFour']

	#save above details to single variable
	api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
	
	#post tweet & image parameter contents
	api.update_status_with_media(status = tweet, media = i)


def new_account(fileName,itemOne,itemTwo,itemThree,itemFour):
# Allows the addition of new API details for future use by this program"""

	fileName = fileName + '.dat'

	save_data = {'itemOne':str(itemOne),'itemTwo':str(itemTwo),'itemThree':str(itemThree),'itemFour':str(itemFour)}
	save_file = open(fileName,'wb')
	pickle.dump(save_data,save_file)
	save_file.close()
