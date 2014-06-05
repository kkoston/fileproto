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
    return {'type': ptype, 'data': pdata}

def hello(params):
    print 'Client connected'

def list_files(params):
    global cur_dir
    packet = make_packet('ls_r', os.listdir(cur_dir[current_thread()]))
    packet_b = msgpack.packb(packet)
    proto.send(packet_b) 
    
def change_dir(params):
    global cur_dir
    cur_dir[current_thread()] = params[0]    

COMMANDS = {
    'ls': list_files,
    'hello': hello,
    'cd': change_dir
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
    
    