"""
  simple datagram
    by li jie

datagram format:
     +--------------+--------------+-------------+------------+-------------+---------------+
     | src IP       | dst IP       | ttl         |  protocol  | length      |  payload      |
     +--------------+--------------+-------------+------------+-------------+---------------+
     |  4 bytes     | 4 bytes      | 1 byte      | 1 byte     | 4 bytes     | 0-546 bytes   |
     
     
     NOTE: the MTU of this datagram is 560 bytes

"""
import struct

import socket

Dgm_Format = "!4s4sBBIs"
MTU = 560
HEADER = 14
PAYLOAD_MTU = 546

class Datagram:
    def __init__(self, ip_src, ip_dst, ttl, ip_proto, payload):
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.ttl = ttl
        self.ip_proto = ip_proto
        self.payload = payload
        
        self.length = len(payload) + HEADER
        
    def pack(self):
        Datagram.pack_datagram(self.ip_src, self.ip_dst, self.ttl, self.ip_proto, self.payload)
    
    @staticmethod
    def pack_datagram(ip_src, ip_dst, ttl, ip_proto, payload:bytes) -> bytes:
        leng = len(payload)
        length = leng + HEADER
        if length > PAYLOAD_MTU:
            raise MTUerror("Datagram should be no longer than 560 bytes!")
        
        datagram = struct.pack('!4s4sBBI%ds' % leng, Datagram.validate(ip_src), Datagram.validate(ip_dst), ttl, ip_proto, length, payload)
        
        return datagram
    def unpack_dartagram(datagram:bytes):
        ip_src, ip_dst, ttl, ip_proto, length= struct.unpack('!4s4sBBI', datagram[:HEADER])
        if length > MTU:
            raise MTUerror("Datagram should be no longer than 560 bytes!")
       
        payload = datagram[HEADER:length]
        return Datagram(ip_src, ip_dst, ttl, ip_proto, payload)
    
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return 'Datagram:\n' + 'ip_src: %(ip_src)s\t' \
              'ip_dst: %(ip_dst)s\n'\
              'ttl: %(ttl)s\n' \
              'ip_proto: %(ip_proto)s\n'\
              'payload: %(payload)s}\n' \
              % self.__dict__
    @staticmethod
    def validate(ip) -> bytes:
        ip_bytes = b''
        if isinstance(ip, str):
            ip_bytes = socket.inet_aton(ip)
        elif isinstance(ip, bytes):
            ip_bytes = ip
        return ip_bytes
            