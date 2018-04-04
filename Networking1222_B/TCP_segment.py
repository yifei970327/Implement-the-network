"""
Simple TCP segment format
+-----------+----------+----------+------------+----------+---------------+------------+-------------+
| src port  | dst port | seq num  | ack num    | flags    | window size   | length     | payload
+-----------+----------+----------+------------+----------+---------------+------------+-------------+
| 2 bytes   | 2 bytes  | 4 bytes  | 4 bytes    | 1 byte   | 2 bytes       | 4 bytes    | 0-527 bytes |
+-----------+----------+----------+------------+----------+---------------+------------+-------------+
|                                              19 bytes                                |
Note:  MTU 546 BYTES
      '!HHIIBHI'
"""
import struct

MTU = 546
HEADER = 19
PAYLOAD_MTU = 527

class TCP_Segment:
    def __init__(self, src_port, dst_port, seq_num, ack_num, flags, win_size, payload):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seq_num  = seq_num
        self.ack_num  = ack_num
        self.flags    = flags  # flags: FIN: 0x1; SYN: 0x2; RST: 0x3; ACK: 0x5, other bits should be zero
        self.win_size = win_size
        self.payload  = payload
        
        #length
        self.length = HEADER + len(payload)
    def pack(self):
        pass
    
    @staticmethod
    def pack_TCPfragment(src_port, dst_port, seq_num, ack_num, flags, win_size, payload:bytes) -> bytes:
        leng = len(payload)
        length = leng + HEADER
        if length > MTU:
            raise MTUerror('TCP length can not be longer than 546 bytes')
        TCPfragment = struct.pack('!HHIIBHI%ds' % leng,src_port, dst_port, seq_num, ack_num, flags, win_size, length, payload )
        return TCPfragment
    @staticmethod
    def unpack_TCPfragment(TCPfragment:bytes):
        src_port, dst_port, seq_num, ack_num, flags, win_size, length = struct.unpack('!HHIIBHI', TCPfragment[:HEADER])
        if length > MTU:
            raise MTUerror('TCP length can not be longer than 546 bytes')
        payload = TCPfragment[HEADER:length]
        return TCP_Segment(src_port, dst_port, seq_num, ack_num, flags, win_size, payload)
    def __repr__(self):
        return self.__str__()
    def __str__():
        return 'TCP_Fragment: \n' + \
               'src_port: %(src_port)s\t' \
               'dst_port: %(dst_port)s\n'\
               'seq_num:  %(seq_num)s\n'\
               'ack_num:  %(acq_num)s\n'\
               'flags  :  %(flags)s\n'\
               'win_size:  %(win_size)s\n'\
               'length:  %(length)s\n'\
               'payload:  %(payload)s\n'\
               % self.__dict__