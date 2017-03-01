import time
import json
import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("[+] {} wrote:".format(self.client_address[0]))
        print("[{}] {}".format(json.loads(data.decode())[1], data.decode()))
        time.sleep(1)
        socket.sendto(data, self.client_address)

if __name__ == "__main__":
    HOST, PORT = "localhost", 2000
    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    print("[+] Create active UDP server")
    print("[+] Ready for communication...")
    server.serve_forever()
    