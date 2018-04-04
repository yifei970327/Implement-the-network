from IP import IPProtocol
import loadConfig

def callback(frame):
    return frame.payload

ip = IPProtocol(loadConfig.loadLocalHostIP(), callback)

# Receiver:
# print(ip.recvdatagram())

# Sender:
ip.senddatagram(loadConfig.loadLocalHostIP(), loadConfig.loadDstIP(), 5, 3, b'mmp')