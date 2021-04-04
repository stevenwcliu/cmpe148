# import socket module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)  # Prepare a server socket

serverPort = 6789
serverSocket.bind(('192.168.0.19', serverPort))
serverSocket.listen(5)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr =  serverSocket.accept()

    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.readlines()
        # Send one HTTP header line into socket
        connectionSocket.send(bytes("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n", 'UTF-8'))
        connectionSocket.send(bytes("\r\n", 'UTF-8'))

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            print(outputdata[i], end = '')
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        connectionSocket.send(bytes("HTTP/ 1.1 404 Not Found\r\n", 'UTF-8'))
        connectionSocket.send(bytes("\r\n", 'UTF-8'))
        connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n", 'UTF-8'))

        connectionSocket.close()


serverSocket.close()
sys.exit()

