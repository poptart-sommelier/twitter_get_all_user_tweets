#!/usr/bin/python3.5

# references:
# https://dev.twitter.com/rest/public/timelines
# http://docs.tweepy.org/en/v3.5.0/api.html

import os
import json
import tweepy
import argparse

CRED_PATH = '/home/rich/.creds/twitter_api.json'

json_data=open(CRED_PATH).read()
creds = json.loads(json_data)

CONSUMER_KEY = creds['twitter_creds'][0]['CONSUMER_KEY']
CONSUMER_SECRET = creds['twitter_creds'][0]['CONSUMER_SECRET']
ACCESS_TOKEN = creds['twitter_creds'][0]['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = creds['twitter_creds'][0]['ACCESS_TOKEN_SECRET']

LAST_ACCESSED_FILE = "./LAST_ACCESSED.txt"

NUMBER_OF_ITEMS = 200
MAX_ID_VAL = None

def twitter_auth():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	_api = tweepy.API(auth)
	return _api

api = twitter_auth()

parser = argparse.ArgumentParser(usage='%(prog)s -u <twitter username>')
parser.add_argument('-u', help='twitter username', dest='user', required=True)
args = parser.parse_args()
twitter_user = args.user

tweets = []

while True:
	statuses = []
	statuses.extend(tweepy.Cursor(api.user_timeline, screen_name=twitter_user, include_entites=True, exclude_replies=True, max_id=MAX_ID_VAL, tweet_mode='extended', include_rts=False).items(NUMBER_OF_ITEMS))

	for x in statuses:
		tweets.append(x.full_text)

	with open(twitter_user+'all_tweets.txt', 'a') as f:
		for tweet in tweets:
			f.write(tweet + '\n')

	if not len(statuses) == 200:
		print("\n... Done!")
		break

	else:
		MAX_ID_VAL = statuses[199].id - 1
