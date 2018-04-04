from LinkLayer import LinkLayer, util
def callback(frame):
    print(frame)
link = LinkLayer(callback)

link.sendto(util.ip2mac("10.20.16.17"), b'hheelekd', None)