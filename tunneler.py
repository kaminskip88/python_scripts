#!/usr/bin/python

import socket
import json
import sys
import subprocess
import psutil

autossh_path='/usr/bin/autossh'
conf_path='/opt/tunneler/tunneler.conf'
monitor_port=21000

def port_free(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = sock.connect_ex(('127.0.0.1', port))
    if res == 0:
        return False
    else:
        return True
        
def assign_port(start_port):
    as_port = start_port
    while True:
        if port_free(as_port) and port_free(as_port+1):
            return as_port
        else:
            as_port += 1
        
#print assign_port(21000)
def read_conf(path):
    try:
        source=open(conf_path)
    except IOError as e:
        sys.exit('ERROR: %s' % e)
    try:
        jsource = json.load(source)
    except ValueError as e:
        sys.exit('Wrong JSON format: %s' %e)
    return jsource

def find_procs(name):
    res_list=[]
    for proc in psutil.process_iter():
        if proc.name() == name:
            res_list.append(proc.cmdline())
    return res_list
 
def proc_match(proc,match1,match2):
    if match1 in proc and match2 in proc:
        return True
    else:
        return False

def is_running(process_list,match1,match2):
    for proc in process_list:
        if proc_match(proc,match1,match2):
            return True
    return False

conf_dict = read_conf(conf_path)
process_list = find_procs('autossh')

for key, value in conf_dict.iteritems():
    match1 = '{0}:{1}:{2}'.format(value['target_port'],value['bind_host'],value['local_port'])
    match2 = '{0}@{1}'.format(value['user'],value['host'])    
    if value['enabled'] == 'True':
        if not is_running(process_list,match1,match2):
            cmd = '{0} -M {1} -f -N -R {2}:{3}:{4} {5}@{6}'.format(autossh_path,assign_port(monitor_port),value['target_port'],value['bind_host'],value['local_port'],value['user'],value['host'])
            subprocess.call(cmd,shell=True)
        else:
            print '%s already up' % key
