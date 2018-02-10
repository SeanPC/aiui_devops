#!/usr/bin/env python
# -*- coding: utf-8 -*-
import SocketServer
import sys
class MyServer(SocketServer.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.sendall('我是多线程')
        Flag = True
        while Flag:
            data = conn.recv(1024)
            print str(conn.getpeername()) + ' : ' + data
            if data == 'kill':
                sys.exit()
            elif data == 'exit':
                conn.sendall('你已经离去')
                Flag = False
            elif data == '0':
                conn.sendall('您输入的是0')
            else:
                conn.sendall('请重新输入.')
if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('0.0.0.0',8002),MyServer)
    server.serve_forever()
    
    