import select
import socket

LOGIN_PREFIX = b"CHAT LOGIN"

class Client():
    def __init__(self, server, client_socket, address):
        self._server = server
        self._socket = client_socket
        self._address = address
        self._name = None
        self._buffer = b""
        print("CLIENT CONNECTED")

    @property
    def socket(self):
        return self._socket

    def close(self):
        self._socket.close()
        self._server.remove_client(self)
        print("CLIENT DISCONECTED")

    def received_message(self, message):
        print(self._name, message)
        self._server.send_message(message)

    def send_message(self, message):
        self._socket.send(message.encode())

    def received(self):
        data = self._socket.recv(1024)
        if not data:
            self.close()
        self._buffer += data
        while b"\n" in self._buffer:
            line, self._buffer = self._buffer.split(b"\n", 1)
            if self._name is None:
                if line.startswith(LOGIN_PREFIX):
                    name = line.removeprefix(LOGIN_PREFIX)
                    if name:
                        self._name = name.decode()
                        print(f"CLIENT LOGIN: {self._name}")
                        continue
                self.close()
                return
            self.received_message(line.decode())

class Server():
    def __init__(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("0.0.0.0", 20000))
        self._server_socket.listen(1)
        self._clients = []
        print("SERVER STARTED")


    def remove_client(self, client):
        self._clients.remove(client)

    def send_message(self, message):
        for client in self._clients:
            client.send_message(message)

    def run(self):
        while True:
            waiting_sockets = [self._server_socket]
            for client in self._clients:
                waiting_sockets.append(client.socket)
            read_sockets = select.select(waiting_sockets, [], [], 5)[0]  #select(caka 5sec na ked sa nieco zmeni na sockete, nieco nacita, niekto nieco posle vtedy sa prikaz zobudi skor)
            if self._server_socket in read_sockets:
                client_socket, address = self._server_socket.accept()
                client = Client(self, client_socket, address)
                self._clients.append(client)
            for client in self._clients:
                if client.socket in read_sockets:
                    client.received()

def main():
    server = Server ()
    server.run()

if __name__ ==  "__main__":
    main()