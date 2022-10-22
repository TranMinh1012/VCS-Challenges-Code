import socket
import sys
import re
import os
import mimetypes

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

def httpget(s,param,url):
    header = ('''GET {url} HTTP/1.1
Host: blogtest.vnprogramming.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
''').format(url=url)+'Cookie: '+param+'\r\n\r\n'
    s.send(header.encode())
    recv = ""
    while True:
        recv += s.recv(4096).decode()
        if "</html>" in recv:
            break
    print(re.findall("<title>(.*?)</title>",recv))
    test = re.search('"multipart_params":.*_wpnonce":"[0-9a-z]+"', recv)
    if test != None:
        nonce = re.search('(?<=_wpnonce":")[0-9a-z]{10}', test.group(0))
        x = nonce.group(0)
        print(x)
        return x

Cookie = []
check = 1

def httppost(s):
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

def httpupload(s):
    wp_nonce = ""
    path = "C:\\Users\\Admin\\Desktop\\image.png"
    content = ""
    file_name = os.path.basename(path)
    file_type = mimetypes.guess_type(path)
    print(file_type[0])
    with open(path,"rb") as f:
        content = f.read()
    print(len(content))
    print(type(content))
    boundary="------WebKitFormBoundaryqLayfr2Tew4zAyKv"
    boundary1 = "------WebKitFormBoundaryqLayfr2Tew4zAyKv"
    cookie_upload=""
    httppost(s)
    if check == 1:    
        for i in Cookie :
            cookie_upload += i+";"
        wp_nonce = httpget(s,cookie_upload,"/wp-admin/media-new.php")
        req_data  = '{b}\r\n'.format(b=boundary)
        req_data  += 'Content-Disposition: form-data; name="_wpnonce"\r\n\r\n{fn}\r\n'.format(fn=wp_nonce)
        req_data  += '{b}\r\n'.format(b=boundary)
        req_data  += 'Content-Disposition: form-data; name="async-upload"; filename="{b}"\r\n'.format(b=file_name)
        req_data  += 'Content-Type: {b}\r\n\r\n'.format(b=str(file_type[0]))
        chunks = req_data
        req_data  += '{b}\r\n'.format(b=content)
        req_data  += '------WebKitFormBoundaryqLayfr2Tew4zAyKv--\r\n'
        lenend = len('------WebKitFormBoundaryqLayfr2Tew4zAyKv--\r\n')
        req = 'POST /wp-admin/async-upload.php HTTP/1.1\r\n'
        req += 'Host: blogtest.vnprogramming.com\r\n'
        req += 'Cookie: {b}\r\n'.format(b=cookie_upload)
        req += 'Content-Length: {b}\r\n'.format(b=str(len(chunks)+len(content)+lenend))
        req += 'Content-Type: multipart/form-data; boundary={b}\r\n'.format(b=boundary1)
        req += 'Accept: */*\r\n'
        req += 'Accept-Encoding: gzip, deflate\r\n'
        req += 'Accept-Language: en-US,en;q=0.9\r\n'
        req += 'Connection: close\r\n'
        req += '\r\n'
        req += chunks
        req = req.encode()
        req += content+b'\r\n'
        req += b'------WebKitFormBoundaryqLayfr2Tew4zAyKv--\r\n'
        print(req)
        s.send(req)
    else:
        return "Upload failed"

httpupload(s)