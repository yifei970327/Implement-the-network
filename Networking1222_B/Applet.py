import threading
import loadConfig
from tkinter import *
from UDP import UDPProtocol

def callback(frame):
  return frame
name = "Alice"
#name = "Bob"

def app_pack(message):
  message = name+": "+message
  return message

def app_repack(message):
  return message

def send():
  message = str(enterBox.get())  # 从调试窗口获取server输入的信息
  message = app_pack(message)
  msgtext.insert(END, "\n{}".format(message))  # update msgtext
  print("{}".format(message))
  enterBox.delete(0, END)  # clear the enterBox
  udp.sendUDP_Fragment(loadConfig.loadPort(), message.encode())

def receive():
  while True:
    message = udp.recvUDP_Fragment().decode()  # recive massage
    message = app_repack(message)
    print("{}".format(message))
    msgtext.insert(END, "\n{}".format(message))  # print message in msgtext
# GUI Initialization
master = Tk()  # build GUI
master.title("{}'s Chat".format(name))  # GUI title
master.geometry("400x650")  # size of GUI
master.resizable(width = True, height = True)  # set GUI size nochangeable
msgtext = Text(master,font = ('Times New Rome', '16', 'bold'), width = 35, height = 29, bd = 4)  # print msg witch already sent on screen
enterBox = Entry(master,font = ('Times New Rome', '16', 'bold'),width = 25,bd = 4)  # the msg you want to send
enterButton = Button(master, text = "SEND", width = 10, height = 4, command = send)  # send button
msgtext.grid(row = 0, column = 0, columnspan = 2, sticky = N + S + W + E)  # make msgtext fill the grid
enterBox.grid(row = 1, column = 0, sticky = N + S + W + E)  # make enterBox fill the grid
enterButton.grid(row = 1, column = 1, padx = 1, pady = 1)  # set button position
print("GUI is ready")  # test sentence

udp = UDPProtocol(callback, loadConfig.loadLocalHostIP(), loadConfig.loadDstIP(), 5000)

# 接收信息线程
t1 = threading.Thread(target = receive)  # add receive_msg to son thread
t1.setDaemon(True)  # protect thread
t1.start()
master.mainloop()
t1.join()

"""
threads = []# 创建threads数组
t1 = threading.Thread(target = send)
threads.append(t1)# 把创建好的线程t1装到threads数组中
t2 = threading.Thread(target = receive)
threads.append(t2)# 把创建好的线程t2装到threads数组中
if __name__  =  =  "__main__":
  for t in threads:
    # t.setDaemon(True) # 将线程声明为守护线程，必须在start()方法前调用，不设置会被无限挂起
    t.start()
  for t in threads:
    t.join()
"""