import socket
import sys
import mimetypes
from urllib.parse import urlparse


if len(sys.argv) <= 1:
    print('Usage : "python team_Martinez_Flores_proxy.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]')
    sys.exit(2)

#Server Socket & Port
ip_Address = sys.argv[1]
serPort = 8888

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind((ip_Address, serPort))
tcpSerSock.listen(1)

print(f"Listening on {ip_Address}:{serPort}\n")

while True:
    print("Ready to serve...\n")
    tcpCliSock, addr = tcpSerSock.accept()
    print(f"Received connection from: {addr}\n")
    message = tcpCliSock.recv(4096).decode()
    print(f"{message}\n")

    url_message_part = message.split()[1]
    print(f"{url_message_part}\n")

    print(urlparse(url_message_part))

    parsed_url = urlparse(url_message_part)

    filename = parsed_url.path.split('/')[-1]

    print(f"{filename}\n")

    fileExist = False
    filetouse = '/' + filename
    print(f"{filetouse}\n")

    try:
        #Check whether the file exist in the cache

        f = open(filetouse[1:], "rb")
        outputdata = f.read()
        f.close()
        fileExist = True
        file_type, _ = mimetypes.guess_type(filetouse[1:])

        #ProxyServer finds a cache hit and generates a response message

        tcpCliSock.send(f"HTTP/1.1 200 OK\r\n".encode())
        tcpCliSock.send(f"Content-Type: {file_type}\r\n".encode())
        tcpCliSock.send(f"Content-Length: {len(outputdata)}\r\n\r\n".encode())
        tcpCliSock.sendall(outputdata)
        print('Read from cache\n')

    except FileNotFoundError:
        print(f"Trying to open: {filename}\n")

        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = parsed_url.path.split('/')[1]
        split_path = parsed_url.path.replace('/', "", 1).split('/', 1)
        path = '/'+ split_path[1]
        print(f"{hostname}\n")
        print(f"{path}\n")

        try:
            c.connect((hostname, 80))
            print(f"Connected to {hostname}\n")

            fileobj = c.makefile("rwb")
            request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
            fileobj.write(request.encode())
            fileobj.flush()

            buffer = fileobj.read()
            print(buffer.decode().split('\r\n'))
            tcpCliSock.sendall(buffer)
            fileobj.close()

            tmpfile = open("./" + filename, "wb")
            tmpfile.write(buffer)
            tmpfile.close()

        except Exception as e:
            print("Illegal request.")

        finally:
            c.close()

    else:
        tcpCliSock.send(f"HTTP/1.1 404 Not Found\r\n".encode())

    finally:
        tcpCliSock.close()