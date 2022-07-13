from logging import error
import socket
import time
import os

host= 'localhost'
port= 5000

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
except ConnectionRefusedError as err:
    print(err, 'it seems that the server is down', sep='\n')
    exit()
print('Connected to server!')
filename= input('filename: ')
path, file_name= os.path.split(filename)
s.send(filename.encode())
content= s.recv(1024)
file= open(file_name, 'wb')
while content:
    print(content.__sizeof__(), 'bytes recived')
    file.write(content)
    content= s.recv(1024)
file.close()
print(content.__sizeof__(), 'bytes recived')
print('file recieved')
s.close()