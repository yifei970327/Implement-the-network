#coding: utf-8
import loadConfig
import time
import threading
from IP import IPProtocol
from TCP_segment import TCP_Segment

TCP_header = 19
sleeptime = 1.5
time_timeout = 5

class TCPProtocol(IPProtocol):
    def __init__(self, callback, src_ip, dst_ip, src_port):
        IPProtocol.__init__(self, src_ip, callback)
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = loadConfig.loadPort()
        self.seq_num = 0
        self.ack_num = 0  # not used
        self.flags = 0
        self.win_size = 1
        self.rcv_seq = 0  # 上次接收到的包的seq_num
        self.if_ret = 0  # 是否接收到了重传的包，用于防止重复打印重传包
        self.if_connect = 0
        # 超时检测线程
        self.cur_time = 0
        self.last_time = time.time()
        self.if_timeout = 0
        # 连续三次收到相同ACK重传
        self.ack_num0 = 999
        self.ack_num1 = 998
        self.ack_num2 = 997
        self.payload0 = ""
        self.payload1 = ""
        self.paylaod2 = ""
        self.seq_num0 = 889
        self.seq_num1 = 888
        self.seq_num2 = 887

    def check_timeout(self):
        while 1:
            time.sleep(0.2)
            if time.time()-self.last_time>time_timeout and self.seq_num>self.ack_num:  # 未收到ACK超时
                print("Timeout!Start retransmission!")
                #print("Config ack#={},seq#={},last time={},time={}".format(self.ack_num,self.seq_num,self.last_time,time.time()))
                self.if_timeout = 1
                self.seq_num = self.seq_num - len(self.payload)
                self.flags = 0
                self.sendTCP_Fragment(self.dst_port, self.seq_num, self.ack_num, self.flags, self.win_size,self.payload)

    def sendTCP_Fragment(self, dst_port, seq_num, ack_num, flags, win_size,payload: bytes):
        self.payload = payload
        if (flags == 0) and(self.if_connect==0):
            self.connect(dst_port)  # 建立连接
        else:
            fragment = TCP_Segment.pack_TCPfragment(self.src_port, self.dst_port, self.seq_num, ack_num, self.flags, win_size, self.payload)
            self.senddatagram(self.src_ip, self.dst_ip, 5, 2, fragment)
            if self.flags == 0:   ### 发送信息
                self.last_time = time.time()
                print("Send Seq#:{},Bytes:{},{}".format(self.seq_num,len(self.payload),self.payload.decode()))
            elif self.flags == 16 and self.if_connect ==1:   ### 发送ACK
                print("Send Ack#:{}".format(ack_num))
            else:
                pass

            self.last_time = time.time()
            self.seq_num = self.seq_num + len(self.payload)
            #print("Config ack#={},seq#={},last time={},time={}".format(self.ack_num,self.seq_num,self.last_time,time.time()))
            self.if_timeout = 0

    def recvTCP_Fragment(self):

        data = None

        while data == None:
            proto, fragment = self.recvdatagram()
            if proto == 2:
                Frag = TCP_Segment.unpack_TCPfragment(fragment)
                if self.src_port == Frag.dst_port:
                    ### 第二次握手
                    if Frag.flags == 2:  # 收到第一次握手：SYN = 1
                        self.ack_num = Frag.seq_num + 1
                        self.seq_num = 0
                        self.flags = 18  # SYN = 1 && ACK = 1
                        self.payload = ""
                        print("Recv 1st handshake")
                        print("    and Sended 2nd handshake")
                        #print("Config ack#={},seq#={},last time={},time={}".format(self.ack_num,self.seq_num,self.last_time,time.time()))
                        time.sleep(sleeptime)
                        self.sendTCP_Fragment(5000, self.seq_num, 233, self.flags, self.win_size,self.payload.encode())
                        continue
                    ### 第三次握手
                    elif Frag.flags == 18:  # 收到第二次握手：SYN = 1 && ACK = 1
                        self.ack_num = Frag.seq_num + 1
                        self.seq_num = 1
                        self.flags = 16  # ACK = 1
                        self.payload = ""
                        print("Recv 2nd handshake")
                        print("    and Send 3rd handshake")
                        #print("Config ack#={},seq#={},last time={},time={}".format(self.ack_num,self.seq_num,self.last_time,time.time()))
                        time.sleep(sleeptime)
                        self.sendTCP_Fragment(5000, self.seq_num, self.ack_num, self.flags, self.win_size,self.payload.encode())
                        self.if_connect = 1
                        continue
                    ### 收到第三次握手
                    elif Frag.flags == 16 and self.if_connect ==0:  # 收到第三次握手：ACK = 1
                        self.seq_num = 1
                        print("Received 3rd handshake")
                        #print("Config ack#={},seq#={},last time={},time={}".format(self.ack_num,self.seq_num,self.last_time,time.time()))
                        self.if_connect = 1
                        continue
                    ### 建立连接后，收到ACK
                    elif Frag.flags == 16 and self.if_connect ==1:
                        self.ack_num2 = self.ack_num1
                        self.ack_num1 = self.ack_num0
                        self.ack_num0 = Frag.ack_num
                        self.payload2 = self.payload1
                        self.payload1 = self.payload0
                        self.payload0 = Frag.payload
                        self.ack_num = Frag.ack_num
                        print("Recv Ack#:{}".format(Frag.ack_num))
                        #print("Config ack#={},seq#={},last time={},time={}".format(self.ack_num,self.seq_num,self.last_time,time.time()))
                        continue
                    ### 收到信息，发送ACK
                    else:
                        self.payload = ""
                        self.flags = 16  # ACK = 1
                        if (Frag.seq_num == self.rcv_seq) and (self.rcv_seq>1):
                            self.if_ret = 1  #
                        self.rcv_seq = Frag.seq_num
                        print("Recv Seq#:{},Bytes:{},{}".format(Frag.seq_num,len(Frag.payload),Frag.payload.decode()))
                        #print("Config ack#={},seq#={},last time={},time={}".format(self.ack_num,self.seq_num,self.last_time,time.time()))
                        time.sleep(sleeptime)
                        self.sendTCP_Fragment(5000, 233, Frag.seq_num + len(Frag.payload), self.flags, self.win_size,self.payload.encode())
                    data = Frag.payload
            """header check    port number,  protocol number"""
        return data
    ### 第一次握手
    def connect(self,dst_port):
        self.seq_num = 0
        self.ack_num = 0  # no use
        self.flags = 2  # SYN = 1
        self.payload = ""
        print("Send 1st handshake")
        self.cur_time = 100*time.time()-int(100*time.time())
        #print("Config ack#={},seq#={},last time={},time={}".format(self.ack_num,self.seq_num,self.last_time,time.time()))
        time.sleep(sleeptime)
        self.sendTCP_Fragment(5000, self.seq_num, self.ack_num, self.flags, self.win_size, self.payload.encode())
        # fragment = TCP_Segment.pack_TCPfragment(self.src_port, dst_port, self.seq_num, 10, flags, self.win_size, payload)
        # self.senddatagram(self.src_ip, self.dst_ip, 5, 2, fragment)  # TCP-like: protocol = 2

    def close(self):
        pass