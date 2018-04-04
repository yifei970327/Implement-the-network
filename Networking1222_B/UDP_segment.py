"""
Simple UDP fragment

fragment format

+-----------+------------+------------+--------------+
| src port  | dst port   | length     | payload      |
+-----------+------------+------------+--------------+
| 2 bytes   | 2 bytes    | 4 bytes    | 0-538 bytes  |
+-----------+------------+------------+--------------+

Note:MTU=538
"""

MTU =546
HEADER=8
PAYLOAD_MTU=538

UDP_Frag_Format = '!HHIs'

import struct
import socket

class UDP_Fragment:
    def __init__(self, src_port, dst_port, payload):
        self.src_port = src_port
        self.dst_port = dst_port
        self.payload = payload
        self.length = len(payload) + HEADER
    def pack(self):
        UDP_Fragment.pack_UDPfragment(self.src_port, self.dst_port, self.payload)
    @staticmethod
    def pack_UDPfragment(src_port, dst_port, payload:bytes)  -> bytes:
        leng = len(payload)
        length = leng+ HEADER
        if length > MTU:
            raise MTUerror("UDP length can not be longer than 546 bytes")
        
        UDPfragment = struct.pack('!HHI%ds' % leng, src_port, dst_port, length, payload)
        return UDPfragment
    @staticmethod
    def unpack_UDPfragment(UDPfragment:bytes):
        src_port, dst_port, length= struct.unpack('!HHI', UDPfragment[:HEADER])
        if length > PAYLOAD_MTU:
            raise MTUerror('UDP length can not be longer than 546 bytes')
        payload = UDPfragment[HEADER:length]
     
        return UDP_Fragment(src_port, dst_port, payload)
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return 'UDP_Fragment: \n' + \
               'src_port: %(src_port)s\t' \
               'dst_port: %(dst_port)s\n'\
               'length:  %(length)s\n'\
               'payload:  %(payload)s}\n'\
               % self.__dict__