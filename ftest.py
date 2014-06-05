import sys
import re
import msgpack
from proto import Proto
import socket

proto = None

def make_packet(ptype, pdata):
    p = {'type': ptype, 'data': pdata}
    return msgpack.packb(p)

def connect(params):
    global proto
    
    if len(params) != 2:
        print "bad syntax"
        return
    host = params[0]
    port = int(params[1])
      
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    proto = Proto(s)
    
    packet = make_packet('hello', None)
    proto.send(packet)    

def list_files(params):
    packet = make_packet('ls', params)
    proto.send(packet)
    
    resp_b = proto.recv()
    resp = msgpack.unpackb(resp_b)
    
    print resp
    return resp

def get_files(params):
    pass
    
def put_files(params):
    pass
    
def make_dirs(params):
    pass

def change_dir(params):
    packet = make_packet('cd', params)
    proto.send(packet)
    
def remove_files(params):
    pass
    
def exit(params):
    sys.exit(0)
    
COMMANDS = {
    'connect': connect,
    'ls': list_files,
    'get': get_files,
    'put': put_files,
    'md': make_dirs,
    'rm': remove_files,
    'cd': change_dir,
    'exit': exit
}

while True:
    cmd_line = raw_input('> ')
    cmd_array = re.split("\s+", cmd_line.strip())
    if not cmd_array[0] in COMMANDS:
        print "Unknown command"
        continue
    else:
        COMMANDS[cmd_array[0]](cmd_array[1:])
    



