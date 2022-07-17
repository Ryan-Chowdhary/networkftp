import socket
import json
import os
import hashlib

data = json.load(open('host.json'))
admin= data['login_detail'][0]
settings= data['service_setting'][0]
host= settings['host']
port= settings['port']
#host= 'localhost'
#port= 5000

def close():
    try:
        s.shutdown(socket.SHUT_RDWR)
        print('~closing connection!')
        s.close()
        exit()
    except Exception as err:
        print(err)        
        exit()

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
    print('server started on', (host, port))
    running= False
except OSError as err:
    print(err)
    print('wait until the service is free\'ed up')
    exit()
    
s.listen(5)
try:
    c, addr = s.accept()
    print('connection recieved from', addr, sep=' ')
    file_tree= os.popen('tree').read()
    c.send(file_tree.encode())
    print(f'file tree sent to client{addr}')
    fname= c.recv(1024)
    fname= fname.decode()
    path, file_name = os.path.split(fname)
    print(f'file requested by client {addr}', file_name, sep=': ')
    file_content = []
    # FILE EXISTS == F.E
    # FILE DOES NOT EXIST == F.NE
    # REQ. FILE IS A DIRECTORY == F.ID
    try:
        file = open(fname, 'rb')
        c.send(b'F.E')
    except FileNotFoundError as err:
        print(err)
        c.send(b'F.NE')
        close()
    except IsADirectoryError as err:
        print(err)
        c.send(b'F.ID')
        close()
    con = ''
    while con != b'':
        con = file.readline(1024)
        file_content.append(con)
    print(f'sending file {file_name} to client {addr}')
    c.send(str(file_content.__len__()).encode())
    for i in file_content:
        #time.sleep(0.01)
        c.send(i)
        print(i.__sizeof__(), 'bytes sent')
    file.close()
    print(f'file {file_name} sent to client {addr}')
    print('verifying file sent to client', addr)
    # Hashing sent file
    sha256_hash = hashlib.sha256()
    for i in file_content:
        sha256_hash.update(i)
    #print(sha256_hash.hexdigest())
    hash = str(sha256_hash.hexdigest())
    c.send(hash.encode())
    new_file_hash = c.recv(1024).decode()
    if str(hash) == str(new_file_hash):
        print('hashes match! File validity confrmed')
    else:
        print('Error, hashes do not match, client has an invalid file.')
    close()
except KeyboardInterrupt as intr:
    print(intr)
    print('aborting!')
    close()
except Exception as err:
    print(err)
    print('aborting!')
    close()