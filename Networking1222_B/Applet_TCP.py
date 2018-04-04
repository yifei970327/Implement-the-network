#coding: utf-8
import threading
import loadConfig
from tkinter import *
from TCP import TCPProtocol

def callback(frame):
  return frame
nameA = "Bob"
nameB = "Alice"

def app_pack(message):
  return message

def app_repack(message):
  return message

def send():
  message = str(enterBox.get())  # 从调试窗口获取server输入的信息
  message = app_pack(message)
  if tcp.if_connect == 1:
    msgtext.insert(END, "\n{}:{}".format(nameA,message))  # update msgtext
  enterBox.delete(0, END)  # clear the enterBox
  tcp.flags = 0
  tcp.sendTCP_Fragment(loadConfig.loadPort(),tcp.seq_num, tcp.ack_num, tcp.flags, tcp.win_size, message.encode())

def receive():
  while True:
    message = tcp.recvTCP_Fragment()
    if tcp.if_connect ==0:
      break
    if tcp.if_ret == 1:
      tcp.if_ret = 0
      break
    if not message == "":
      message = message.decode()  # recive massage
      message = app_repack(message)
      msgtext.insert(END, "\n{}:{}".format(nameB,message))  # print message in msgtext

# GUI Initialization
master = Tk()  # build GUI
master.title("{}'s Chat".format(nameA))  # GUI title
master.geometry("550x730")  # size of GUI
master.resizable(width = True, height = True)  # set GUI size nochangeable
msgtext = Text(master,font = ('Times New Rome', '20', 'bold'), width = 35, height = 24, bd = 4)  # print msg witch already sent on screen
enterBox = Entry(master,font = ('Times New Rome', '20', 'bold'),width = 25,bd = 4)  # the msg you want to send
enterButton = Button(master, text = "SEND", width = 10, height = 2, command = send)  # send button
msgtext.grid(row = 0, column = 0, columnspan = 2, sticky = N + S + W + E)  # make msgtext fill the grid
enterBox.grid(row = 1, column = 0, sticky = N + S + W + E)  # make enterBox fill the grid
enterButton.grid(row = 1, column = 1, padx = 1, pady = 1)  # set button position

tcp = TCPProtocol(callback, loadConfig.loadLocalHostIP(), loadConfig.loadDstIP(), 5000)
# 接收信息线程
t1 = threading.Thread(target = receive)  # add receive_msg to son thread
t2 = threading.Thread(target=tcp.check_timeout)
t1.setDaemon(True)  # protect thread
t1.start()
t2.start()
master.mainloop()
t1.join()
t2.join()
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