import socket
import sys

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

header = ('''GET /wp-content/uploads/2022/10/image.jpg HTTP/1.0
HOST: blogtest.vnprogramming.com\r\n\r\n''')
s.sendall(header.encode())
reply = b''
while True:
    chuck = s.recv(1024)
    if len(chuck) == 0:
        break
    reply = reply+chuck
reply = reply.split(b"\r\n\r\n")[1]
print("Kich thuoc file anh: " + str(len(reply)))
f = open('image.png','wb') 
f.write(reply)
f.close()