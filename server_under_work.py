#!/usr/bin/env python3

import wolframalpha
import os
import sys
import socket
#sudo apt-get install espeak
#sudo apt-get install espeak python-espeak

#!/usr/bin/env python3

"""
A simple echo server
"""

import socket

host = ''
port = int(sys.argv[2])
backlog = int(sys.argv[4])
size = int(sys.argv[6])

app_id = "U2UH86-RKRWT8E9W9"
client = wolframalpha.Client(app_id)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
print('Waiting for a question...')

while 1:
	cli, address = s.accept()
	data = cli.recv(size)
	os.system('espeak "{}" 2>/dev/null'.format(data))
	res = client.query(data)
	answer = next(res.results).text
	if data:
		cli.send(str.encode(answer))
		cli.close()
