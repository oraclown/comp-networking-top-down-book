from socket import *
import sys

server_socket = socket(AF_INET, SOCK_STREAM)
# prepare a server socket
server_socket.bind(('', 8081))
server_socket.listen(1)

while True:
    # Establish the connection
    print("Ready to serve...")
    connection_socket, addr = server_socket.accept()

    try:
        message = connection_socket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        # Send one HTTP header line into socket
        connection_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connection_socket.send(outputdata[i].encode())
        connection_socket.send("\r\n".encode())
        connection_socket.close()
    
    except IOError:
        # Send response message for file not found
        connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connection_socket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # Close client socket
        connection_socket.close()

server_socket.close()
sys.exit()