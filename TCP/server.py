import socket
import select

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(("0.0.0.0", 20000))
serv_socket.listen(1)
sockets = [serv_socket]
while True:
    read_sockets = select.select(sockets,[],[],5)[0]
    if serv_socket in read_sockets:
        client_soc , add = serv_socket.accept()
        print(f"Pripojeny klient: {add}")
        sockets.append(client_soc)
    elif read_sockets:
        client_soc = read_sockets[0]
        buf = client_soc.recv(1024)
        if buf:
            print(f"Prijate data: {buf}")
            client_soc.send(buf + b" : odpovedam")
        else:
            print("Zatvaram klienta")
            client_soc.close()
            sockets.remove(client_soc)
