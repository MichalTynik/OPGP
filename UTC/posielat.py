import socket
import json

y=json.dumps(x)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(x, ("127.0.0.1", 25000))