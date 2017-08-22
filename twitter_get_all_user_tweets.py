#!/usr/bin/python3.5

# references:
# https://dev.twitter.com/rest/public/timelines
# http://docs.tweepy.org/en/v3.5.0/api.html

import os
import json
import tweepy
import argparse
import queue
import threading
import unshorten_links

# THIS IS USED TO RETRIEVE LOCALLY STORED CREDENTIALS
CRED_PATH = '/home/rich/.creds/twitter_api.json'

json_data=open(CRED_PATH).read()
creds = json.loads(json_data)

CONSUMER_KEY = creds['twitter_creds'][0]['CONSUMER_KEY']
CONSUMER_SECRET = creds['twitter_creds'][0]['CONSUMER_SECRET']
ACCESS_TOKEN = creds['twitter_creds'][0]['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = creds['twitter_creds'][0]['ACCESS_TOKEN_SECRET']

# BOOKMARK FILE TO RETAIN LAST ACCESSED TWEET.
LAST_ACCESSED_FILE = "./LAST_ACCESSED.txt"

# MAX NUMBER OF TWEETS TO RETRIEVE (API RESTRICTIONS MANDATE THIS)
NUMBER_OF_ITEMS = 200
MAX_ID_VAL = None

# THIS HANDLES TWITTER AUTH TOKENS
def twitter_auth():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	_api = tweepy.API(auth)
	return _api

# THREADED FUNCTION - UNSHORTENS LINKS
def get_and_unshort_urls(i):
	for j in i.entities['urls']:
		r = unshorten_links.unshorten(j['expanded_url'])
		url_dict[j['url']] = r
		print("Found: " + j['url'] + " Matches: " + r)

# GET A TOKEN
api = twitter_auth()

# READ THE COMMAND LINE
parser = argparse.ArgumentParser(usage='%(prog)s -u <twitter username>')
parser.add_argument('-u', help='twitter username', dest='user', required=True)
args = parser.parse_args()
twitter_user = args.user

tweets = []
url_dict = {}

while True:
	statuses = []
	statuses.extend(tweepy.Cursor(api.user_timeline, screen_name=twitter_user, include_entites=True, exclude_replies=True, max_id=MAX_ID_VAL, tweet_mode='extended', include_rts=False).items(NUMBER_OF_ITEMS))

	threads = []

	for x in statuses:
		t = threading.Thread(target=get_and_unshort_urls, args=(x,))
		threads.append(t)

	for x in threads:
		x.start()

	for x in threads:
		x.join()

#	tweets.append(x.full_text)
	for x in statuses:
		for y in x.entities['urls']:
			if y['url'] in url_dict:
				tweets.append(x.full_text.replace(y['url'], url_dict[y['url']]))

	with open(twitter_user+'all_tweets.txt', 'a') as f:
		for tweet in tweets:
			f.write(tweet + '\n')

	if not len(statuses) == 200:
		print("\n... Done!")
		break

	else:
		MAX_ID_VAL = statuses[199].id - 1

	url_dict.clear()
