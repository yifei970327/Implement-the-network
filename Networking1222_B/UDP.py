from IP import IPProtocol
from UDP_segment import UDP_Fragment

UDP_header = 8
class UDPProtocol(IPProtocol):
    def __init__(self, callback, src_ip, dst_ip, src_port):
        IPProtocol.__init__(self, src_ip, callback)
        self.src_port = src_port
        self.dst_ip = dst_ip

    def sendUDP_Fragment(self, dst_port, payload:bytes):
        fragment = UDP_Fragment.pack_UDPfragment(self.src_port, dst_port, payload);
        """
            How to allocate dst_IP
        """
        self.senddatagram(self.src_ip, self.dst_ip, 5, 3, fragment)
        
    def recvUDP_Fragment(self):
        
        data = None
        
        while data == None:
            """
            HOW TO USE protocol number in this case
            """
            port, fragment = self.recvdatagram()
            if port == 3:
                Frag = UDP_Fragment.unpack_UDPfragment(fragment)
                if self.src_port == Frag.dst_port:
                    data = Frag.payload
                
            """
              header check    port number,  protocol number
            """
            
        return data
            
            
        """"
            Something should be done to get the UDP_segment
        """