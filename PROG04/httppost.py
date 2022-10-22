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

Cookie = []

# connecting to server
s.connect((host_ip, 80))

check = 1

payload="log=test&pwd=test123QWE%40AD&rememberme=forever&wp-submit=Log+In&redirect_to=https%3A%2F%2Fblogtest.vnprogramming.com%2Fwp-admin&testcookie=1"
header = ('''POST /wp-login.php HTTP/1.1
Host: blogtest.vnprogramming.com
Origin: https://blogtest.vnprogramming.com
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: wordpress_test_cookie=WP%20Cookie%20check; wp_lang=en_US
''')+"Content-Length: "+str(len(payload))+"\r\n\r\n"+payload+"\r\n\r\n"

header = header.encode()
s.send(header)
recv = s.recv(8000).decode()
if re.findall("HTTP/1.1 \d+ Found",recv):
    print("User test dang nhap thanh cong")
    x= re.findall("Set-Cookie: ([^;]+);?",recv)
    for i in x:
        Cookie.append(i)     
else :
    check=0
    print("User test dang nhap that bai")