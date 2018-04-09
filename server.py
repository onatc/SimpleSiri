#!/usr/bin/env python3

import wolframalpha
import serverKeys
import os
import sys
import socket
import pickle
import hashlib
from cryptography.fernet import Fernet

host = ''
port = int(sys.argv[2])
backlog = int(sys.argv[4])
size = int(sys.argv[6])

client = wolframalpha.Client(serverKeys.wolfram_alpha_appid)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
print('[Checkpoint] Created socket at 0.0.0.0 on port',port,'\n')
print('[Checkpoint] Listening for client connections\n')
s.listen(backlog)

while 1:
	cli, address = s.accept()
	print('[Checkpoint] Accepted client connection from',address[0],'on port',port,'\n')
	data = cli.recv(size)
	print('[Checkpoint] Received data: ',data,'\n')
	
	data_tuple = pickle.loads(data)
	key = data_tuple[0]
	question_enc = data_tuple[1]
	checksum = data_tuple[2]
	# Check checksum
	if (hashlib.md5(question_enc).hexdigest() != checksum):
		print('[Checkpoint] Checksum is INVALID\n')
	else:
		print('[Checkpoint] Checksum is VALID\n')

		# Decrypt
		f = Fernet(key)
		question_dec = f.decrypt(question_enc)
		print('[Checkpoint] Decrypt: Using Key:',key,'\nPlaintext:',question_dec,'\n')

		question = question_dec.decode('utf-8')
		print('[Checkpoint] Speaking:',question,'\n')
		os.system('espeak "{}" 2>/dev/null'.format(question))

		print('[Checkpoint] Sending question to Wolfram Alpha:',question,'\n')
		res = client.query(question)

		answer = next(res.results).text
		print('[Checkpoint] Received answer from Wolfram Alpha: ',answer,'\n')
		if answer:
			# Encrypt
			answer_enc = f.encrypt(str.encode(answer))
			print('[Checkpoint] Encrypt: Generated Key:',key,'\nCiphertext:',answer_enc,'\n')
			
			checksum = hashlib.md5(answer_enc).hexdigest()
			print('[Checkpoint] Generated MD5 Checksum:',checksum,'\n')

			data = (answer_enc, checksum)
			payload = pickle.dumps(data)

			print('[Checkpoint] Sending data:',payload,'\n')
			cli.send(payload)
			
	cli.close()
