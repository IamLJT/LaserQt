# -*- coding: utf-8 -*-
from socket import *

def main():
    host = "192.168.1.102"
    port = 80
    addr = (host, port)
    bufferSize = 1024 

    while True:
        tcpClientSock = socket(AF_INET, SOCK_STREAM)
        tcpClientSock.connect(addr)

        sendData = input('>> ')
        if not sendData:
            break
        else:
            tcpClientSock.send("{}\r\n".format(sendData).encode("utf-8"))
        
        recvData = tcpClientSock.recv(bufferSize).decode("utf-8")
        if not recvData:
            break
        else:
            print(recvData.strip())
        
        tcpClientSock.close()

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))   
