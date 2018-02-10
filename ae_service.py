#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys,logging,importlib,os,ConfigParser

#initialize config loading
config_path = '/root/code/python/ae.conf'
CONFIG = ConfigParser.ConfigParser(allow_no_value=True)
CONFIG.read(config_path)
pid_file = '/tmp/ae.pid'
logfile = '/tmp/ae_client.log'


def Readconfig(section,key=None):
    #import pdb;pdb.set_trace()
    if not CONFIG:
        print "Invalid config file."
        sys.exit(1)
    if section not in CONFIG.sections():
        print "Can not find section %s in config file." % section
        sys.exit(1)
    if key == None:
        return CONFIG.options(section)
    elif key not in CONFIG.options(section):
        print "Key %s doesn't exist for section %s." % (key,section)
        sys.exit(1)
    else:
        return CONFIG.get(section,key)

def log(level,message):
    if debug == 'yes' and level != 'debug':
        return
    mylog = getattr(logging,level)
    mylog(message)
class AEpid(object):
    def write(self,file):
        pid = str(os.getpid())
        with open(file,'w') as f:
            f.write(pid)
    def get(self,file):
        with open(file,'r') as f:
            return f.read()
    def remove(self,file):
        if os.path.exists(file):
            os.remove(file)
def usage():
    print "Usage:client.py {start|stop|restart|status}"

debug = Readconfig('logger','debug')
if debug == 'yes':
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=logfile,
            filemode='a+')
else:
    logging.basicConfig(level=logging.INFO,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=logfile,
            filemode='a+')
