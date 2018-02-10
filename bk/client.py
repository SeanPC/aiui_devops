#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
ip_port = ('192.168.164.21',8002)
sk = socket.socket()
#sk.bind(("127.0.0.1",8010))
sk.connect(ip_port)
while True:
    data = sk.recv(1024)
    print 'receive:',data
    inp = raw_input('please input:')
    sk.sendall(inp)
    if inp == 'exit':
        break
sk.close()
