#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
from threading import Thread
import threading


class SocketWrapper(object):

    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr

    def rec_data(self):
        try:
            return self.sock.recv(1024).decode('utf-8')
        except:
            return ''

    def client_info(self):
        return self.addr

    def send_data(self, msg):
        return self.sock.sendall(msg.encode('utf-8'))

    def close(self):
        self.sock.close()


class BasicSocket(socket.socket):
    
    def __init__(self, ip_port):
        self.ip_port = ip_port
        super(BasicSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(self.ip_port)
        self.listen(20)


class MyServer(object):

    def __init__(self):
        self.ip_port = (socket.gethostname(), 9999)
        self.sk = BasicSocket(self.ip_port)
        self.clients = set()
        self.clients_lock = threading.Lock()

    def start_server(self):

        while True:
            print('服务器等待连接...')
            conn, addr = self.sk.accept()
            client_data = SocketWrapper(conn, addr)
            with self.clients_lock:
                self.clients.add(client_data)
            t = Thread(target=self.start_thread, args=(client_data,))
            t.start()
            print('客户端已加入', addr)
            print('当前已经加入客户端数量：%s' % str(len(self.clients)))

    def start_thread(self, client_data):
        while True:
            msg, info = client_data.rec_data(), client_data.client_info()
            print(msg, info)
            if not msg:
                client_data.close()
                self.clients.remove(client_data)
                print(len(self.clients))
                break

            elif msg == 'what':
                with self.clients_lock:
                    self.all_user()

            else:
                hello = '你好:%s, 我是服务器' % msg
                client_data.send_data(hello)

    def all_user(self):
        for c in self.clients:
            print(c)
            c.send_data('all')


if __name__ == '__main__':
    ms = MyServer()
    ms.start_server()
