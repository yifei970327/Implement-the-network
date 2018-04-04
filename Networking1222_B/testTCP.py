from TCP import TCPProtocol
import loadConfig

def callback(frame):
    return frame.payload
TCP = TCPProtocol(callback, loadConfig.loadLocalHostIP(), loadConfig.loadDstIP(), 800)

### Sender:
TCP.sendTCP_Fragment(loadConfig.loadDstPort(), b'I am sending TCP')
### Receiver:
#print(TCP.recvTCP_Fragment())