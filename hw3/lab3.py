from socket import *
import ssl
import base64
import time

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

tlsCommand = 'STARTTLS\r\n'
tlsCommand = tlsCommand.encode()
clientSocket.send(tlsCommand)
recv2 = clientSocket.recv(1024).decode()
print("Message after STARTTLS command:" + recv2)
clientSocket = ssl.wrap_socket(clientSocket)

# Authentication
username =  "anna.nana2332@gmail.com"
password =  "ananana123!@#"
base64_str = ("\x00"+username+"\x00"+password).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024).decode()
print("After AUTH command: " + recv_auth)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: <anna.nana2332@gmail.com>\r\n"
clientSocket.send(mailFrom.encode())
recv3 = clientSocket.recv(1024).decode()
print("After MAIL FROM command: " + recv3)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <anna.nana2332@gmail.com>\r\n"
clientSocket.send(rcptTo.encode())
recv4 = clientSocket.recv(1024).decode()
print("After RCPT TO command: " + recv4)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
data = "DATA\r\n"
clientSocket.send(data.encode())
recv5 = clientSocket.recv(1024).decode()
print("After DATA command: " + recv5)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send message data.
subject = "Subject: SMTP Client\r\n\r\n" 
clientSocket.send(subject.encode())
date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
date = date + "\r\n\r\n"
clientSocket.send(date.encode())
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024).decode()
print("Response after ending the message:" + recv_msg)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
quit = "QUIT\r\n"
clientSocket.send(quit.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)
clientSocket.close()
