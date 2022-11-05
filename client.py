#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import os
import time

ip_port = (socket.gethostname(), 9999)

sk = socket.socket()
sk.connect(ip_port)
sk.sendall('{}'.format(os.getlogin()).encode('utf-8'))
server_reply = sk.recv(1024).decode()
print(server_reply)

while True:
    name = input('你可以输入：')
    client_data = '%s' % name
    sk.sendall(client_data.encode('utf-8'))
    server_reply = sk.recv(1024).decode()
    print(server_reply)
    if server_reply == 'all':
        for i in range(1,10):
            time.sleep(0.1)
            print(i)


