# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:30:21 2020

@author: LKC
"""

import matplotlib.pyplot as plt
import socket
import sys
import threading
import time



def server():

    
    def bind():
        HOST = '192.168.43.62'
        port = 777
        s.bind((HOST, port))

    def listen():
        s.listen(5) # 最大等待数
        print('Socket now listening')

    def send(conn):
        while True:
            try:
                sth = input('message send:\n')
                if sth=='q':
                   conn.close()
                   break
                conn.sendall(sth.encode('utf-8'))
            except ConnectionError:
                print('connect error')
                conn.close()
                sys.exit(0)
            except:
                print('unexpect error')
                conn.close()
                sys.exit(0)

    def recv(conn):
        # plt.ion()
        # plt.figure(1)
        
        x=range(64)
        pitch=[0]*64
        roll=[0]*64
        yaw=[0]*64

        
        while True:
            try:
                
                data = conn.recv(1024)
                data = data.decode()
                data = data.split('+')
                # data = data.decode('utf-8')
                # print(data)
            

                for i in range(len(roll)-1):
                        yaw[i]=yaw[i+1]
                        pitch[i]=pitch[i+1]
                        roll[i]=roll[i+1]

                # if data[1]=='  -' :
                #     data[1]='0'
                # if data[2]=='  -' :
                #     data[2]='0'

                pitch[63]=float(data[0])/10
                roll[63]=float(data[1])/10
                yaw[63]=float(data[2])/10

                # plt.subplot(211)
                plt.plot(x,roll,color='red',label='roll')
                plt.plot(x,pitch,color='green',label='pitch')
                plt.plot(x,yaw,color='blue',label='yaw')
                plt.legend()
                plt.draw()
                plt.pause(0.1)


            except ConnectionError:
                print('connect error')
                conn.close()
                sys.exit(0)
            except:
                print('unexpect error')
                conn.close()
                sys.exit(0)



    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind()
    listen()
    conn, addr = s.accept()
    print("connect success")
    print('connect time: ' + time.ctime())
    threading._start_new_thread(recv, (conn,))
    send(conn)


if __name__ == '__main__':
    server()