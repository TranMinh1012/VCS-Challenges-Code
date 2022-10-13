import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print ("Socket successfully created")
except socket.error:
	print ("socket creation failed with error %s" %(socket.error))

# Socket default port
port = 80

try:
	host_ip = socket.gethostbyname('blogtest.vnprogramming.com')
except socket.gaierror:

	# Could not resolve the host
	print ("there was an error when resolving the host")
	sys.exit()

# connecting to server
s.connect((host_ip, port))

request = "GET / HTTP/1.1\r\nHost: ' + 'blogtest.vnprogramming.com' + '\r\n\r\n"
s.sendall(request.encode())

response = s.recv(4096).decode()

title = ''
for line in response.split('\n'):
    if "<title>" in line:
        start = line.find('<title>')
        end = line.find('</title>')
        for i in range(start + 7, end):
            title = title + line[i]
        break

print(f"Title: {title[0:10]}")

s.close()