
import socket
import time
import os

host= 'localhost'
port= 5000

def close():
    try:
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        exit()
    except Exception as err:
        s.close()
        print('wait until the service is free\'ed up')
        exit()

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
running= True
while running:
    try:
        s.bind((host, port))
        print('server started on', (host, port))
        running= False
    except OSError as err:
        print(err)
        s.close()
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
    try:
        file = open(fname, 'rb')
        c.send(b'F.E')
    except FileNotFoundError as err:
        print(err)
        c.send(b'F.NE')
        print('~closing connection!')
        close()
    con = ''
    while con != b'':
        con = file.readline(1024)
        file_content.append(con)
    print(f'sending file {file_name} to client {addr}')
    for i in file_content:
        #time.sleep(0.01)
        c.send(i)
        if i.__sizeof__() >= 1024:
            print(i.__sizeof__(), 'bytes sent')
    file.close()
    print(f'file {file_name} sent to client {addr}')
    close()
except KeyboardInterrupt as intr:
    print(intr)
    print('aborting!')
    close()
except Exception as err:
    print(err)
    print('aborting!')
    close()