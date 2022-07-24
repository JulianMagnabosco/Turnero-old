from concurrent.futures import thread
from select import select
import socket
import sys
import threading

class ConectionServer:
    def __init__(self, update):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = 8000
        self.ADDRESS = "0.0.0.0"
        self.broadcast_list = []
        self.my_socket.bind((self.ADDRESS, self.PORT))
        self.message_list = []
        self.update = update
        self.alive = True
        # self.action0 = action0
        # self.action1 = action1
        # self.action2 = action2

    def loop(self, data):
        while self.alive:
            self._loop(data)


    def _loop(self, data):
        self.my_socket.listen()
        client, client_address = self.my_socket.accept()
        self.broadcast_list.append(client)
        client.send(data.encode())
        print("serchin")
        self.start_listenning_thread(client)
        # try:
        #     self.client, self.client_address = self.my_socket.accept()
        #     self.broadcast_list.append(self.client)
        #     self.start_listenning_thread(self.client)
        # except:
        #     pass
        
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
                else: 
                    self.message_list.append(message)
                    self.update(message)
                    #print(self.message_list)
                    # if str(message).rfind('0') >= 0:
                    #     self.action0(str(message).removeprefix('0'))
                    # if str(message).rfind('1') >= 0:
                    #     self.action1(str(message).removeprefix('1'))
                    # if str(message).rfind('2') >= 0:
                    #     self.action2(str(message).removeprefix('2'))
                self.broadcast(message)
            else:
                print(f"client has been disconnected : {name}")
                self.broadcast(client)
                return
        
    def broadcast(self,message):
        for client in self.broadcast_list:
            try:
                client.send(message.encode())
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
        

