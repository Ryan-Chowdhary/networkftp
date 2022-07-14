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
    print(err, 'it seems that the server is down or unreachable', sep='\n')
    exit()
print('Connected to server!')
file_tree= s.recv(2048*10)
file_tree= file_tree.decode('utf-8', 'ignore')
print(file_tree)
filename= input('filename: ')
path, file_name= os.path.split(filename)
s.send(filename.encode())
    # FILE EXISTS == F.E
    # FILE DOES NOT EXIST == F.NE
try:
    file_status= s.recv(1024)
    if file_status.decode() == 'F.E':
        pass
    elif file_status.decode() == 'F.NE':
        s.close()
        print('file does not exist on server')
        print('~server disconnected!')
        exit()
except Exception as err:
    print(err, 'an exception has occured at line 19', sep='\n')
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