#!/usr/bin/env python
# -*- coding: utf-8 -*-
import SocketServer,signal,time,socket
import sys
class MyServer(SocketServer.BaseRequestHandler):
    def handle(self):
        down_sk = self.request
        up_sk = socket.socket()
        remote_ip_port = ('192.168.164.21',8009)
        up_sk.connect(remote_ip_port)
        client = down_sk.getpeername()[0]
        while True:
            if client_exit == 1:
                down_sk.sendall('yes')
            elif client_exit == 2:
                down_sk.close()
            else:
                down_sk.sendall('no')
            
            data = down_sk.recv(1024)
            #data = client + ' : ' + data
            print data
            up_sk.sendall(data)
            if data == 'exit':
                print 'Client %s is leaving' % client
                break
        up_sk.close()
        down_sk.close()


#main code
        
client_exit = 0
server = SocketServer.ThreadingTCPServer(('0.0.0.0',8002),MyServer)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print 'exit'
finally:
    client_exit = 1
    time.sleep(5)
    #need check if client exist, and close them by set client_exit = 2
    server.server_close()