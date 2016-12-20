import json
import socket
import sys

HOST, PORT = "localhost", 9999
data = ['0x01', 1, 1.2, 1.2, 2.4, 2.4, 700, 350, 0]


# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
sock.sendto(bytes(json.dumps(data), "utf-8"), (HOST, PORT))
received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(json.loads(received)[1]))
