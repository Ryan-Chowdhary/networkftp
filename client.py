import socket
import json
import os
import hashlib
import time

data = json.load(open('../host.json'))
settings= data['service_setting'][0]
host= settings['host']
port= settings['port']
#host= 'localhost'
#port= 5000

def close():
    try:
        s.close()
        print('~server disconnected!')
        exit()
    except Exception:
        exit()

def create_dir(dir):
    try:
        os.mkdir(dir)
        os.chdir(dir)
    except FileExistsError:
        os.chdir(dir)

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
except ConnectionRefusedError as err:
    print(err, 'it seems that the server is down or unreachable', sep='\n')
    s.close()
    exit()
print('Connected to server!')
file_tree= s.recv(2048*10).decode('utf-8', 'ignore')
print(file_tree)
filename= input('filename: ')
path, file_name= os.path.split(filename)
s.send(filename.encode())
# FILE EXISTS == F.E
# FILE DOES NOT EXIST == F.NE
# REQ. FILE IS A DIRECTORY == F.ID
try:
    file_status= s.recv(1024)
    if file_status.decode() == 'F.E':
        pass
    elif file_status.decode() == 'F.NE':
        print('file does not exist on server')
        close()
    elif file_status.decode() == 'F.ID':
        print('requested file is a directory!')
        close()
except Exception as err:
    print(err, 'an exception has occured at line 19', sep='\n')

file_id, file_ext = os.path.splitext(file_name)
file_contents_list = []

create_dir(file_id)

file= open(file_name, 'wb')
#length = s.recv(1024).decode()
#print(length)
while True:
    content= s.recv(1024)
    if content==b'end':
        break
    file_contents_list.append(content)
    print(content.__sizeof__(), 'bytes recived')
    file.write(content)
file.close()
print('file recieved')
# Hashing recived file
print('verifying integrity of recived file')
sha256_hash = hashlib.sha256()
for i in file_contents_list:
    sha256_hash.update(i)
new_file_hash = str(sha256_hash.hexdigest())
original_hash = s.recv(1024).decode()
s.send(new_file_hash.encode())
print(new_file_hash, original_hash, sep='\n')
if str(new_file_hash) == str(original_hash):
    print('hashes match! File validity confrmed')
else:
    print('Error, hashes do not match, it seems that you have recived an bad file.')

close()
