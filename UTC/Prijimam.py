import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 25000))
while True:
    data, addr = sock.recvfrom(100)
    vypis = json.loads(data)
    print(f"Recv: {addr}, Message: {vypis}")
