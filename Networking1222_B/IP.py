"""
IP protocol


"""

IPheader = 14
import loadConfig
from datagram import Datagram

from LinkLayer import LinkLayer
from LinkLayer import util

from socket import * 
class IPProtocol(LinkLayer):
    
    
    def __init__(self, src_ip, callback):
        linkLayer=LinkLayer.__init__(self, callback)
        
        self.src_ip = src_ip
    
        #self.payload = None
        #self.received_UDP_TCP = False
    
    
    """
    """
    def senddatagram(self, ip_src, ip_dst, ttl, ip_proto, data):
        datagram = Datagram.pack_datagram(ip_src, ip_dst, ttl, ip_proto, data)
        
        
        ##   Here, let's set dst_mac according to our program >>>>
        dst_mac = util.ip2mac(loadConfig.loadDstIP())
        self.sendto(dst_mac, datagram, None)
        """  how to acquire dst_mac"""
    
    def recvdatagram(self):
        data = None
        protocol = 0
        while data == None :
            if self.received == True:
                datagram = self.payload
                gram = Datagram.unpack_dartagram(datagram)
               # print(gram.ip_dst)
                if self.src_ip == inet_ntoa(gram.ip_dst):
                    data = gram.payload
                    protocol = gram.ip_proto
                self.received = False
            """ here need us to add a header check , check localip ==dst_ip"""
            """I think that here we need to reserve the protocol number"""
        return protocol, data
    
    
    