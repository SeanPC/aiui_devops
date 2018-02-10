#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket,sys,commands,json,re,time,signal,ConfigParser,os
is_exit = 0
aepath = '/root/code/aiui_devops'
sys.path.append(aepath)
from ae_service import *
pid = AEpid()


def getData():
    hostname = socket.gethostname()
    rc,out = commands.getstatusoutput('ifconfig -a')
    for i in out.split('\n\n'):
        if '192.168' in i:
            ip = re.findall(r'inet (.+?) ',i)[0]
            return {"hostname":hostname,"ip":ip}
def signal_handler(signum, frame):
    global is_exit
    is_exit = 1

def start():
    print '\nStarting AE client...',
    if Readconfig('agent','agent') == 'yes':
        section = 'agent'
    else:
        section = 'server'
    remote_ip_port = (Readconfig(section,'host'),int(Readconfig(section,'port')))
    local_ip_port = ("0.0.0.0",int(Readconfig('client','port')))
    sk = socket.socket()
    sk.bind(local_ip_port)
    try:
        sk.connect(remote_ip_port)
        pid.write(pid_file)
        print 'Done!'
        log('info','Succesful to start AE client.')
        log('debug','Succesful to conenct server %s from %s' % (remote_ip_port,local_ip_port)) 
    except Exception as e:
        log('debug','Failed to conenct server %s from %s as reason %s' % (remote_ip_port,local_ip_port,str(e)))
        sys.exit(1)
    while True:
        try:
            data = sk.recv(1024)
            print data
            if data == 'exit':
                is_exit = '1'
        except:
            pass
        data0 = json.dumps(getData())
        sk.sendall(data0)
        time.sleep(1)
        if is_exit == 1:
            sk.sendall('exit')
            time.sleep(1)
            break
    sk.close()

def stop():
    print '\nStopping AE client...',
    commands.getoutput('kill -14 %s' % pid.get(pid_file))
    time.sleep(2)
    pid.remove(pid_file)
    print 'Done!'
   
    
signal.signal(signal.SIGALRM, signal_handler)
try:
    cmd = sys.argv[1]
except IndexError,e:
    usage()
    sys.exit(1)
if cmd == 'start':
    start()
elif cmd == 'stop':
    stop()
else:
    usage()