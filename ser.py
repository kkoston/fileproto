import socket
import msgpack
import os
from proto import Proto
from threading import Thread, current_thread

HOST = '127.0.0.1'
PORT = 5011
client_threads = []
proto = None
cur_dir = {}

def make_packet(ptype, pdata):
    p = {'type': ptype, 'data': pdata}
    return msgpack.packb(p)

def hello(params):
    print 'Client connected'

def list_files(params):
    global cur_dir
    packet = make_packet('ls_r', os.listdir(cur_dir[current_thread()]))
    proto.send(packet) 
    
def make_dirs(params):
    global cur_dir
    d = cur_dir[current_thread()]
    nd = params[0]
    
    if nd[0] != '/':
        nd = os.path.normpath(os.path.join(d, nd))
    
    if not os.path.exists(nd):
        os.makedirs(nd)
        packet = make_packet('md_r', 'OK')
    else:
        packet = make_packet('md_r', 'dir exists')   
    
    proto.send(packet)    
        
def change_dir(params):
    global cur_dir
    d = cur_dir[current_thread()]
    nd = params[0]
    
    if nd[0] != '/':
        nd = os.path.normpath(os.path.join(d, nd))
    
    if not os.path.exists(nd):
        print "no dir"
        packet = make_packet('cd_r', 'no dir')
        proto.send(packet)
        print "error packet sent "
        return False
    
    cur_dir[current_thread()] = nd
    
    print nd
    packet = make_packet('cd_r', 'OK')
    proto.send(packet)    
    return True  

COMMANDS = {
    'ls': list_files,
    'hello': hello,
    'cd': change_dir,
    'md': make_dirs
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)

def handle_client(afd):
    global proto
    proto = Proto(afd)    
    
    cur_dir[current_thread()] = os.getcwd()
    
    while True:
        resp_b = proto.recv()
        if resp_b == "":
            print "Client disconnected"
            return
        resp = msgpack.unpackb(resp_b)
        
        COMMANDS[resp['type']](resp['data']) 
        

while True:
    afd, addr = s.accept()
    t = Thread(target=handle_client, args=(afd,))
    t.setDaemon(True)
    t.start()
    client_threads.append(t)
    
    