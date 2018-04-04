from IP import IPProtocol
def callback(frame):
    return frame.payload

ip = IPProtocol("192.168.1.125", callback)

#print(ip.recvdatagram())
ip.senddatagram("192.168.1.125", "192.168.1.120", 5, 3, b'mmp')