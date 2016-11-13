# -*- coding: utf-8 -*-
from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)
import time

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2016.11.08
'''

def current_time():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))

class LaserQtRequestHandler(SRH):
    def handle(self):
        print("客户端 < {} > 已经连接!".format(self.client_address))
        revcData = self.rfile.readline().decode("utf-8").strip()
        self.wfile.write(("{}".format("0.1, 0.1, 0.3, 0.3, 0")).encode("utf-8"))
        
def main():
    host = "0.0.0.0"
    port = 80
    addr = (host, port)
    newTCPServer = TCP(addr, LaserQtRequestHandler)
    print("等待客户端的连接...")
    newTCPServer.serve_forever()

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))
