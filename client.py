#!/usr/bin/env python3

import socket
import sys
import os
from cryptography.fernet import Fernet
import tweepy
from tweepy.streaming import StreamListener
import json
import hashlib
import pickle
import clientKeys

host = str(sys.argv[2])
port = int(sys.argv[4])
size = int(sys.argv[6])
hashtag = str(sys.argv[8])

ACCESS_TOKEN = clientKeys.access_token
ACCESS_SECRET = clientKeys.access_token_secret
CONSUMER_KEY = clientKeys.consumer_key
CONSUMER_SECRET = clientKeys.consumer_secret

# Twitter streaming adapted from: http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html

class listener(StreamListener):
    def on_data(self, data_1):
        all_data = json.loads(data_1)
    
        if 'text' in all_data:
            tweet = all_data["text"]
            print('[Checkpoint] New Tweet: ',tweet,'\n')
            tweet_parsed = tweet.replace(hashtag, '')
            
            key = Fernet.generate_key()
            f = Fernet(key)
            question_enc = f.encrypt(str.encode(tweet_parsed))
            print('[Checkpoint] Encrypt: Generated Key:',key,'\nCiphertext:',question_enc,'\n')
            checksum = hashlib.md5(question_enc).hexdigest()
            print('[Checkpoint] Generated MD5 Checksum:',checksum,'\n')
        
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('[Checkpoint] Connecting to',host,'on port',port,'\n')
            s.connect((host,port))
        
            data = (key, question_enc, checksum)
            payload = pickle.dumps(data)
        
            print('[Checkpoint] Sending data:',payload,'\n')
            s.send(payload)
        
            rec_data = s.recv(size)
            print('[Checkpoint] Received data:',rec_data,'\n')
            s.close()
        
            data_tuple = pickle.loads(rec_data)
            answer_enc = data_tuple[0]
            checksum = data_tuple[1]
            if (hashlib.md5(answer_enc).hexdigest() != checksum):
                print('[Checkpoint] Checksum is INVALID\n')
            else:
                print('[Checkpoint] Checksum is VALID\n')
            
                answer_dec = f.decrypt(answer_enc)
                print('[Checkpoint] Decrypt: Using Key:',key,'\nPlaintext:',answer_dec,'\n')
                answer = answer_dec.decode('utf-8')
            
                print('[Checkpoint] Speaking:',answer,'\n')
                os.system('espeak "{}" 2>/dev/null'.format(answer))


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)

myStream = tweepy.Stream(auth, listener())
print('[Checkpoint] Listening for Tweets that contain:',hashtag,'\n')
myStream.filter(track=[hashtag])