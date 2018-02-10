#!/usr/bin/env python
# -*- coding: utf-8 -*-
import SocketServer,signal,time
import sys
class MyServer(SocketServer.BaseRequestHandler):
    def handle(self):
        conn = self.request
        client = str(conn.getpeername())
        while True:
            if client_exit == 1:
                conn.sendall('yes')
            elif client_exit == 2:
                conn.close()
            else:
                conn.sendall('no')
            data = conn.recv(1024)
            print client + ' : ' + data
            if data == 'exit':
                print 'Client %s is leaving' % client
                break
        conn.close()
        
client_exit = 0
server = SocketServer.ThreadingTCPServer(('0.0.0.0',8002),MyServer)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print 'exit'
finally:
    client_exit = 1
    time.sleep(5)
    #need check if exist client, and close them by set client_exit = 2
    server.server_close()