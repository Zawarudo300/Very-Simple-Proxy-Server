# Very-Simple-Proxy-Server
This project is a TCP server socket that is bound to the IP address the user
enters into the command terminal and port number 8888, in which it listens for a
connection from a client. The TCP server socket awaits for a connection from a TCP client 
socket and once it receives one, it decodes its message. Note: this proxy server only works 
with the GET command and will throw an error for other HTTP requests. Also, the HTTP GET request
provided by the client must be typed out in its format. The server then gets the URL from the 
client's message and parses it in order to get the name of the file requested from the client. 
The server then tries to find the file in its cache (i.e. the folder where the code is located) 
and if it finds it, it sends a HTTP response message to the client that contains it. If the server
doesn't find it in the cache, then it creates a TCP socket on itself and connects it to the host 
server that has the file, in which doing so it forwards the client's message to it. The server will 
then get the response back from the host and forward it to the client. Afterwards, the server will 
then create a cache file on itself that contains the file the host sent back. The server will then
close its socket to the host. If the server still cannot find the file requested by the client 
after searching its cache and requesting the host for it, then it sends an HTTP Not Found message to 
the client. The server will then finally close the clients connection to it and await for another client
to connect to it.
