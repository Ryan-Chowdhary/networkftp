import socket
import time
import os

host= 'localhost'
port= 5000

def close():
    try:
        s.close()
        exit()
    except Exception:
        exit()

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except OSError as err:
    print(err)
    exit()
s.listen(5)
try:
    c, addr = s.accept()
    print('connection recieved from', addr, sep=' ')
    fname= c.recv(1024)
    fname= fname.decode()
    path, file_name = os.path.split(fname)
    print(f'file requested by client {addr}', file_name, sep=': ')
    file_content = []
    try:
        file = open(fname, 'rb')
    except FileNotFoundError as err:
        print(err)
        s.close()
        exit()
    con = ''
    while con != b'':
        con = file.readline()
        file_content.append(con)
    print(f'sending file {fname} to client {addr}')
    for i in file_content:
        #time.sleep(0.01)
        c.send(i)
        print(i.__sizeof__(), 'bytes sent')
    file.close()
    time.sleep(0.5)
    print(f'file {file_name} sent to client {addr}')
except KeyboardInterrupt as intr:
    print(intr)
    print('aborting!')
    close()
except Exception as err:
    print(err)
    print('aborting!')
    close()