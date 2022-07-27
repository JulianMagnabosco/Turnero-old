import socket

class ConectionClient:
    def __init__(self,address,port):
        self.nickname = "local"
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address# "127.0.1.1"
        self.port = port
        self.my_socket.connect((self.address, self.port))
        self.data = self.my_socket.recv(1024).decode()
        self.my_socket.send(f'@{self.nickname}'.encode())

    def send(self,message):
        self.my_socket.send(message.encode())
        return self.my_socket.recv(1024).decode()
        

