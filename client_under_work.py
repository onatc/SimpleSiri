#!/usr/bin/env python3

"""
A simple echo client
"""

import socket
import sys
import tweepy
from tweepy.streaming import StreamListener
import json

host = str(sys.argv[2])
port = int(sys.argv[4])
size = int(sys.argv[6])
hashtag = str(sys.argv[8])
		
ACCESS_TOKEN = '4851547798-h7wF6P5cf2HdSGlj6hCUJvJTLLhzA82UrIBAZf5'
ACCESS_SECRET = 'lu9gtoFHq3fX68IYe3K0NXIGgAkwN3rlS7F0FmwoVw9oe'
CONSUMER_KEY = 'doVfxMxW9PY01ueak3fynqHHO'
CONSUMER_SECRET = 'uyiZh0CR95ziZDqMzenGHIAEMNVq9oWgr4b9ZOxA07aRisJMek'


class listener(StreamListener):
	def on_data(self, data_1):
		all_data = json.loads(data_1)
		
		if 'text' in all_data:
			tweet = all_data["text"]
			tweet = tweet.replace(hashtag, '')
			
			print(tweet)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host,port))
			
			tweet_fix = str.encode(tweet)		
			s.send(tweet_fix)
			
			data = s.recv(size)
			data_fix = data.decode('utf-8')
			
			print(data_fix)
			s.close()



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)

myStream = tweepy.Stream(auth, listener())
myStream.filter(track=[hashtag])


