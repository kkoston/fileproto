import struct
from socket import MSG_PEEK

class Proto():
    FMT = '<l'
    BUFSZ = 1024
    
    def __init__(self, s):
        self.sock = s
    
    def send(self, buff):
        #print 'SEND: ' + buff
        packet_size = len(buff)
        size_struct = struct.pack(self.FMT, packet_size)
        buff = size_struct + buff
        
        buff_len = len(buff)
        total = 0
        while total < buff_len:
            bs = self.sock.send(buff[total:])
            if bs == 0:
                return 0
            total = total + bs 
        
        return total  
        
    def recv(self):
        total = 0
        buff = ''
        br = 0
        while (br < 4):
            buff = self.sock.recv(self.BUFSZ, MSG_PEEK)
            if len(buff) == 0:
                return ''
            br = len(buff)
        
        size_struct = self.sock.recv(4);
        packet_size = struct.unpack(self.FMT, size_struct)[0]
        
        #print 'Expected packet size %d' % packet_size

        buff = ''
        while total < packet_size:
            #print 'Total %d ' % total
            tmp_buff = self.sock.recv(self.BUFSZ, MSG_PEEK)
            tmp_buff_len = len(tmp_buff)
            #print 'Peeked len %d' % tmp_buff_len
            
            # if received part of exactly the whole packet
            if tmp_buff_len + total <= packet_size:
                buff = buff + tmp_buff
                total = total + tmp_buff_len
                self.sock.recv(tmp_buff_len)
            # received more than this packet length
            else:
                buff = buff + self.sock.recv(packet_size - total)
                total = total + packet_size
        #print 'RECV: ' + str(len(buff))      
        return buff
    



