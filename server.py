#!/usr/bin/env python
# -*- coding: utf-8 -*-
import SocketServer,signal,time
import sys
class MyServer(SocketServer.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.sendall('Welcome to join into AE!')
        client = str(conn.getpeername())
        while True:
            print client_exit
            if client_exit == 1:
                conn.sendall('exit')
            data = conn.recv(1024)
            print client + ' : ' + data
            if data == 'exit':
                print 'Client %s is leaving' % client
                break
            time.sleep(1)

def signal_handler(signum, frame):
    global client_exit
    client_exit = 1
client_exit = 0
signal.signal(signal.SIGALRM, signal_handler)
server = SocketServer.ThreadingTCPServer(('0.0.0.0',8002),MyServer)
server.serve_forever()
# try:
    # server.serve_forever()
# except KeyboardInterrupt:
    # print 'exit'
# finally:
    # client_exit = 1
    # time.sleep(5)
    # server.server_close()