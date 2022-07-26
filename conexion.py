import socket,threading
import sys
from turtle import update

class ConectionServer:
    def __init__(self, update):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = 8000
        self.ADDRESS = "0.0.0.0"
        self.broadcast_list = []
        self.my_socket.bind((self.ADDRESS, self.PORT))
        self.update = update
        self.alive = True
        self.data = ""

    def loop(self, data):
        while self.alive:
            self._loop(data)


    def _loop(self, data):
        # self.my_socket.listen()
        # print("serchin")
        # client, client_address = self.my_socket.accept()
        # self.broadcast_list.append(client)
        # client.send(data.encode())
        # self.start_listenning_thread(client)
        # self.my_socket.settimeout(0.1)
        try:
            self.my_socket.listen()
            self.update("")
            client, client_address = self.my_socket.accept()
            self.broadcast_list.append(client)
            client.send(data.encode())
            self.data = data
            self.start_listenning_thread(client)
            self.my_socket.settimeout(0.1)
        except:
            pass
        
    def start_listenning_thread(self,client):
        self.client_thread = threading.Thread(
                target=self.listen_thread,
                args=(client,) #the list of argument for the function
        )
        self.client_thread.start()
    

    def listen_thread(self,client):
        name = ""
        while self.alive:
            message = client.recv(1024).decode()
            if message:
                if str(message).rfind('@') >= 0:
                    print(f"New client: {str(message).removeprefix('@')}")
                    name = str(message).removeprefix('@')
                elif message !="[]": 
                    self.data = self.update(message)
                self.broadcast()
            else:
                print(f"client has been disconnected : {name}")
                if len(self.broadcast_list)-1 <= 0:
                    self.alive = False
                    self.my_socket.close()
                return
        
    def broadcast(self):
        for client in self.broadcast_list:
            try:
                client.send(self.data.encode())
            except:
                self.broadcast_list.remove(client)
                print(f"Client removed : {client}")
        if len(self.broadcast_list) <= 0:
            self.alive = False
            self.my_socket.close()
                

class ConectionClient:
    def __init__(self):
        self.nickname = "local"
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost" # "127.0.1.1"
        self.port = 8000
        self.my_socket.connect((self.host, self.port))
        self.data = self.my_socket.recv(1024).decode()
        self.my_socket.send(f'@{self.nickname}'.encode())

    def send(self,message):
        self.my_socket.send(message.encode())
        return self.my_socket.recv(1024).decode()
        

