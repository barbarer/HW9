# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # still need this in the same directory, filled out

# The function get_tweets searches for all tweets created by the user "umsi" and 
# all tweets that mention "umsi"
# It caches the data and will use the cached data if it exists
def get_tweets(api, cacheDict, fname):

	# if the data is in the dictionary return it
	searchTerm = "umsi"
	if searchTerm in cacheDict:
		print("Using data from cache")
		
	# otherwise get the data, add it the dictionary, and write it to a file
	else:
		print("Fetching tweets")

		# get tweets by the umsi user
		tweetDictList1 = api.user_timeline(searchTerm)
		
		# get tweets that mention umsi
		dict =  api.search(q=searchTerm)
		tweetDictList2 = dict.get("statuses", None)

		# add both to the dictionary
		cacheDict[searchTerm] = tweetDictList1 + tweetDictList2

		# write out the ditionary as JSON
		dumped_json_cache = json.dumps(cacheDict)
		fw = open(fname,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		
	# return the list of tweets
	return cacheDict[searchTerm]


## [PART 1]
# 
# Finish the function setUpTweetTable that takes a list of tweets, a sqlite connection object, and a cursor and inserts the tweet information in the database
# Create a database: tweets.sqlite,
# Load all of the tweets into a database table called Tweets, with the following columns in each row:
## tweet_id - containing the unique id that belongs to each tweet
## author - containing the screen name of the user who posted the tweet (note that even for RT'd tweets, it will be the person whose timeline it is)
## time_posted - containing the date/time value that represents when the tweet was posted (note that this should be a TIMESTAMP column data type!)
## tweet_text - containing the text that goes with that tweet
## retweets - containing the number that represents how many times the tweet has been retweeted
def setUpTweetTable(tweetList, conn, cur):

	# Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), 
	# with the correct (5) column names and appropriate types for each.
	# HINT: Remember that the time_posted column should be the TIMESTAMP data type!
	
	# Use a for loop, the cursor you defined above to execute INSERT statements, that insert the data from each of the tweets in umsi_tweets into the correct columns in each row of the Tweets database table.

	#  Use the database connection to commit the changes to the database
	pass

## [PART 2]

# Finish the function getTimeAndText that returns a list of strings that contain the 
# time_posted and the text of the tweets.  It takes a database cursor as input.
# Select the time_posted and tweet_text from the Tweets table in tweets.sqlite and return a list 
# of strings that contain the date/time and text of each tweet in the form: date/time - text as shown below
# Mon Oct 09 16:02:03 +0000 2017 - #MondayMotivation https://t.co/vLbZpH390b
def getTimeAndText(cur):
	
	# create a list to hold the strings 
	
	# select the time_posted and tweet_text from Tweets and add it to the list of strings
	
	# return the list of the tweet information in string form
	pass
	
# Finish the function getAuthorAndNumRetweets that returns a list of strings for the tweets that have been retweeted MORE than 2 times
# It takes a database cursor as input.
# Select the author (screen name) and number of retweets for of all of the tweets that have been retweeted MORE than 2 times
# Return a list of strings that are in the form: author - # retweets as shown below
# umsi - 5
def getAuthorAndNumRetweets(cur):
	
	# create a list to hold the strings 
	
	# select the author and number of retweets from the Tweets table where the number of retweets is > 2
	pass

'''		
def tweetsPerDayOfWeek(cur):

	# create an emply dictionary

	# select time_posted for all the tweets and analyze the first three characters to determine the day of the week
	# then populate the dictionary tweetDays with the number of tweets that occur on each day

	# return dictionary
'''

## Unittests to test the functions
class TestHW9(unittest.TestCase):
	def setUp(self):
		consumer_key = twitter_info.consumer_key
		consumer_secret = twitter_info.consumer_secret
		access_token = twitter_info.access_token
		access_token_secret = twitter_info.access_token_secret
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		
		# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

		# And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching.
		fname = "twitter_cache.json"
		try:
			cache_file = open(fname,'r')	
			cache_contents = cache_file.read()
			cache_file.close()
			cacheDict = json.loads(cache_contents)
		except:
			cacheDict = {}
			
		self.conn = sqlite3.connect('tweets.sqlite')
		self.cur = self.conn.cursor()
		self.tweetList = get_tweets(api, cacheDict, fname)
		
	def test_setUpTweetTable(self):
		setUpTweetTable(self.tweetList, self.conn, self.cur)
		self.cur.execute('SELECT * FROM Tweets')
		self.assertEqual(35, len(self.cur.fetchall()))
		
	def test_getTimeAndText(self):
		strList = getTimeAndText(self.cur)
		self.assertEqual(len(strList), 35)
		self.assertEqual(strList[0], 'Tue Nov 13 22:02:48 +0000 2018 - Meet MSI student Huyen Phan and the team that created Peerstachio, the social network and learning community that a… https://t.co/Wyivz99Y73')
		
	def test_getAuthorAndNumRetweets(self):
		strList2 = getAuthorAndNumRetweets(self.cur)
		self.assertEqual(len(strList2), 6)
		self.assertEqual(strList2[0], '1062380175306964992 - umsi - 5')

	'''
	def test_extraCredit(self):
		tweetDict = tweetsPerDayOfWeek(self.cur)
		correctTweetDict = {'Tue ': 27, 'Mon ': 5, 'Sun ': 1, 'Sat ': 1, 'Fri ': 1}
		self.assertEqual(tweetDict,correctTweetDict)
	'''

if __name__ == "__main__":
	unittest.main(verbosity=2)