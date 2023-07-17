import tkinter as tk
from basic import Basic
import time
import socket
from tkinter import *



ipEntry = None
portEntry = None
teamAEntry = None

# 自动博弈
def start():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((ipEntry.get(), int(portEntry.get())))
    message = sk.recv(1024).decode("utf-8")
    if message == "name":
        Basic.my_print("TeamName: " + teamAEntry.get())
        Basic.my_print("--------------------------------")
        # 发送队名
        sk.send(str(teamAEntry.get()).encode())

        # 记录已经赢下的筹码量
        alreadyWinChips = 0

        # 开始比赛，共70局
        i = 0

        while True:

            i = i % 70

            if i == 0:
                # 记录已经赢下的筹码量
                alreadyWinChips = 0
                Basic.to_file_str = ""

            # while True:
            Basic.my_print("----------- 第" + str(i + 1) + "局 ----------------")

            start = time.time()

            tempWinChips,winLowLimit = Basic.basic(sk,alreadyWinChips,i + 1)

            end = time.time()

            if ((end - start )) >= 60:
                print("time!!!!!")

            alreadyWinChips += tempWinChips
            Basic.my_print("alreadyWinChips :" + str(alreadyWinChips))

            # 计算稳赢需要的最小筹码量
            winNeedMinChips = ((70 - (i + 1)) * 75 + winLowLimit) - alreadyWinChips

            Basic.my_print("winNeedMinChips :" + str(winNeedMinChips))

            opWinMinChips = ((70 - (i + 1)) * 75) + alreadyWinChips
            Basic.my_print("opWinMinChips :" + str(opWinMinChips))

            i += 1

            if i == 70:
                Basic.to_file(alreadyWinChips)



#手动博弈
def start_handle():
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((ipEntry.get(), int(portEntry.get())))
    message = sk.recv(1024).decode("utf-8")
    if message == "name":
        print("TeamName: " + teamAEntry.get())
        print("--------------------------------")
        # 发送队名
        sk.send(str(teamAEntry.get()).encode())

        message = sk.recv(1024).decode("utf-8")
        print(message)
        while True:
            strs = input()
            sk.send(strs.encode())
            message = sk.recv(1024).decode("utf-8")
            print(message)


root = tk.Tk()  # 生成一个主窗口
root.title("骑士德州扑克")
width = 450  # 设置窗口的宽度
height = 300  # 设置窗口的长度
size = '%dx%d+%d+%d' % (width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2)
root.geometry(size)  # 将窗口居中
root.resizable(0,0)

'''参赛队名'''
head = tk.Frame(root, width=450, height=30)
# teamA
Label(head, fg='black', text='TeamA: ', font=('楷书', 12), height=3, width=10).place(anchor=W, rely=0.35)
team1 = StringVar()
teamAEntry = Entry(head, textvariable=team1)
teamAEntry.place(relx=0.15, rely=0.025)
team1.set("KnighTeam-TP2")
# teamB
Label(head, fg='black', text='TeamB: ', font=('楷书', 12), height=3, width=10).place(anchor=W, relx=0.50, rely=0.35)
team2 = StringVar()
teamBEntry = Entry(head, textvariable=team2)
teamBEntry.place(relx=0.64, rely=0.025)
head.place(rely=0.05)

'''端口号和IP地址'''
neck = tk.Frame(root, width=450, height=50)
# ServerIp
Label(neck, fg='black', text='ServerIp: ', font=('楷书', 12), height=3, width=17).place(anchor=W, relx=-0.03, rely=0.7)
ip = StringVar()
ipEntry = Entry(neck, textvariable=ip, width=16)
ipEntry.place(relx=0.21, rely=0.5)
# ip.set("127.0.0.1")
# ip.set("123.56.15.98")
# ServerPort
Label(neck, fg='black', text='ServerPort: ', font=('楷书', 12), height=3, width=18).place(anchor=W, relx=0.46, rely=0.7)
port = StringVar()
portEntry = Entry(neck, textvariable=port, width=14)
portEntry.place(relx=0.73, rely=0.5)
port.set("10001")
neck.place(rely=0.2)


'''按钮'''
body = tk.Frame(root, width=450, height=50)
# connect
connect = Button(body, text='Connect', font=('楷书', 12), height=2, width=8, command=start)
connect.place(anchor=W, relx=0.1, rely=0.5)

# start
connect_handle = Button(body, text='Connect_handle', font=('楷书', 12), height=2, width=15, command=start_handle)
connect_handle.place(anchor=E, relx=0.9, rely=0.5)

body.place(relx=0, rely=0.5)

'''底部信息'''
foot = tk.Frame(root, width=300, height=25)
Label(foot, fg='black', text='copyright: CQUT.303 GameLab', font=('楷书', 10), height=2).place(anchor=W, rely=0.3)
foot.place(relx=0.3, rely=0.85)

# ip.set("39.99.226.85")
ip.set("127.0.0.1")
# ipEntry.insert('end', '127.0.0.1')

# start_handle()
start()
# root.mainloop()

