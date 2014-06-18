import sys
import re
import msgpack
from proto import Proto
import socket

proto = None

def make_packet(ptype, pdata):
    p = {'type': ptype, 'data': pdata}
    return msgpack.packb(p)

def recv():
    resp_b = proto.recv()
    resp = msgpack.unpackb(resp_b)
    print "recvd", resp
    return resp
    
def send(packet):
    proto.send(packet)

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
    send(packet)  

def list_files(params):
    packet = make_packet('ls', params)
    send(packet)    
    resp = recv()
    
    return resp

def get_files(params):
    pass
    
def put_files(params):
    pass
    
def make_dirs(params):
    packet = make_packet('md', params)
    send(packet)
    resp = recv()

def change_dir(params):
    packet = make_packet('cd', params)
    send(packet)
    resp = recv()
    
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

if sys.argv[1] == 'connect':
    connect(sys.argv[2:])

while True:
    cmd_line = raw_input('> ')
    cmd_array = re.split("\s+", cmd_line.strip())
    if not cmd_array[0] in COMMANDS:
        print "Unknown command"
        continue
    else:
        COMMANDS[cmd_array[0]](cmd_array[1:])
    



