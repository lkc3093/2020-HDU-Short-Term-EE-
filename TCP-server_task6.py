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
        adc=[0]*64
        ax=[0]*64
        ay=[0]*64
        az=[0]*64
        bx=[0]*64
        by=[0]*64
        bz=[0]*64
        
        while True:
            try:
                
                data = conn.recv(1024)
                data = data.decode()
                data = data.split('+')
                # data = data.decode('utf-8')
                print(data)

                for i in range(len(adc)-1):
                        adc[i]=adc[i+1]
                        ax[i]=ax[i+1]
                        ay[i]=ay[i+1]
                        az[i]=az[i+1]
                        bx[i]=bx[i+1]
                        by[i]=by[i+1]
                        bz[i]=bz[i+1]


                adc[63]=int(data[1])
                ax[63]=int(data[2])
                ay[63]=int(data[3])
                az[63]=int(data[4])
                bx[63]=int(data[5])
                by[63]=int(data[6])
                bz[63]=int(data[7])



                # plt.subplot(211)
                plt.plot(x,adc,color='red',label='adc')
                plt.plot(x,ax,color='green',label='ax')
                plt.plot(x,ay,color='blue',label='ay')
                plt.plot(x,az,color='skyblue',label='az')
                plt.plot(x,bx,color='darkolivegreen',label='bx')
                plt.plot(x,by,color='black',label='by')
                plt.plot(x,bz,color='cornsilk',label='bz')
                plt.legend()
                plt.draw()
                plt.pause(0.1)


            except ConnectionError:
                print('connect error')
                conn.close()
                sys.exit(0)
            except:
                print('unexpect error')
                bx[63]=int(data[5])
                by[63]=int(data[6])
                bz[63]=int(data[7])
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