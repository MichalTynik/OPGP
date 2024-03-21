import PyQt6.QtWidgets
import PyQt6.QtCore
import socket
import datetime
import select

class Okno(PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Okno")
        self.setGeometry(100,100,400,300)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 20000))
        
        central_widget = PyQt6.QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = PyQt6.QtWidgets.QVBoxLayout(central_widget)

        self.history = PyQt6.QtWidgets.QListWidget()
        layout.addWidget(self.history)

        input_layout = PyQt6.QtWidgets.QHBoxLayout()

        self.add = PyQt6.QtWidgets.QLineEdit("127.0.0.1")
        input_layout.addWidget(self.add)  # Higher stretch factor for self.add

        self.mes = PyQt6.QtWidgets.QLineEdit("Ahoj")
        self.mes.returnPressed.connect(self.btn_pressed)
        input_layout.addWidget(self.mes, 2)

        self.btn = PyQt6.QtWidgets.QPushButton("Odoslat")
        self.btn.clicked.connect(self.btn_pressed)
        input_layout.addWidget(self.btn)

        layout.addLayout(input_layout)

        self.timer = PyQt6.QtCore.QTimer(self)
        self.timer.timeout.connect(self.recv)
        self.timer.start(1000)
        self.show()
        
    def btn_pressed(self):
        message = self.mes.text()
        self.sock.sendto(message.encode(), (self.add.text(), 20000))
        
    def recv(self):
        while True:
            self.read_sockets = select.select([self.sock],[],[],0)[0]
            if self.read_sockets:
                data, add = self.sock.recvfrom(100)
                cas = datetime.datetime.now().strftime("%H:%M:%S")
                self.history.addItem(f"{cas} - {add[0]} - {data.decode()}")
            else:
                return
            

app = PyQt6.QtWidgets.QApplication([])
win = Okno()
app.exec()
