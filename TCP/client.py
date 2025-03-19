import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.10.62", 5678))
sock.send("CHAT LOGIN MAREK\n".encode())
sock.send("tajná správa\n".encode())
print(sock.recv(1024).decode())
sock.close()
