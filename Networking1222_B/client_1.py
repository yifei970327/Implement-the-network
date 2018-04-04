import threading
from socket import *
from tkinter import *

name = 'B'
self_ip = '192.168.1.125'
receive_port = 2003
send_port = 2004
target_name = ''
target_ip = '192.168.1.120'
target_port = 2001


def analysis_message(message):  # give a str the first_part is username second is hostip third is post
    global target_name, target_ip, target_port
    target_name = message.split()[0]
    target_ip = message.split()[1]
    target_port = message.split()[2]
    i = len(target_name) + len(target_ip) + len(target_port) + 2
    msg = message[i:len(message)]
    return (target_name, target_ip, int(target_port), msg)


def receive_msg():  # recive massage function
    global target_name, target_ip, target_port
    receive_socket = socket(AF_INET, SHUT_RDWR)  # build sokect
    receive_socket.bind((self_ip, receive_port))
    print('{} accept_msg is ready'.format(name))  # confirm sokect was built
    while 1:
        message = udp.recvUDP_Fragment().decode()  # translate bytes to string
        target_name, target_ip, target_port, msg = analysis_message(message)  # update var
        msgtext.insert(END, '\n{} :{}'.format(target_name, msg))  # print message in msgtext


def send_msg():  # send message function
    send_socket = socket(AF_INET, SHUT_RDWR)  # build sokect
    send_socket.bind((self_ip, send_port))
    print('{} send_msg is ready'.format(name))  # confirm sokect was built
    msg_s = str(enterBox.get())  # get massage from enterBox
    message = name + ' ' + self_ip + ' ' + str(receive_port) + ' ' + msg_s  # add imformation to message
    msgtext.insert(END, '\n{}:{}'.format(name, msg_s))  # update msgtext
    send_socket.sendto(message.encode(), (target_ip, target_port))  # send message
    enterBox.delete(0, END)  # clear the enterBox


master = Tk()  # build GUI
master.title("{}'s Chat".format(name))  # GUI title
master.geometry("400x500")  # size of GUI
master.resizable(width=False, height=False)  # set GUI size nochangeable
msgtext = Text(master, width=50, height=25, bd=4)  # print msg witch already sent on screen
enterBox = Entry(master)  # the msg you want to send
enterButton = Button(master, text="SEND", width=10, height=4, command=send_msg)  # send button
msgtext.grid(row=0, column=0, columnspan=2, sticky=N + S + W + E)  # make msgtext fill the grid
enterBox.grid(row=1, column=0, sticky=N + S + W + E)  # make enterBox fill the grid
enterButton.grid(row=1, column=1, padx=1, pady=1)  # set button position
print("GUI is ready")  # test sentence

t1 = threading.Thread(target=receive_msg)  # add receive_msg to son thread
t1.setDaemon(True)  # protect thread
t1.start()
master.mainloop()
t1.join()