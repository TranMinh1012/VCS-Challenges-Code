import socket
import sys
import re

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print ("Socket successfully created")
except socket.error:
	print ("socket creation failed with error %s" %(socket.error))

try:
	host_ip = socket.gethostbyname('blogtest.vnprogramming.com')
except socket.gaierror:

	# Could not resolve the host
	print ("there was an error when resolving the host")
	sys.exit()

# connecting to server
s.connect((host_ip, 80))

header = '''GET / HTTP/1.1
Host: blogtest.vnprogramming.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
''' + '\r\n\r\n'

s.send(header.encode())
recv = ""
while True:
	recv += s.recv(4096).decode()
	if "</html>" in recv:
		break
title = re.findall("<title>(.*?)</title>",recv)
print(f"Title: {title[0][0:10]}")

s.close()