from select import select
import socket
import threading

class ConectionServer:
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = 8000
        self.ADDRESS = "0.0.0.0"
        self.broadcast_list = []
        self.my_socket.bind((self.ADDRESS, self.PORT))
        self.my_socket.setblocking(False)

    def loop(self):
        self.my_socket.listen()
        try:
            self.client, self.client_address = self.my_socket.accept()
            self.broadcast_list.append(self.client)
            self.start_listenning_thread(self.client)
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
        message = None
        while True:
            try:
                message = client.recv(1024).decode()
            except:
                print("error")
            if message:
                if str(message).rfind('@') >= 0:
                    print(f"New client: {str(message).removeprefix('@')}")
                    name = str(message).removeprefix('@')
                else: 
                    print(f"Received message : {message}")
                    self.broadcast(message)
            else:
                print(f"client has been disconnected : {name}")
                return
        
    def broadcast(self,message):
        for client in self.broadcast_list:
            try:
                client.send(message.encode())
            except:
                self.broadcast_list.remove(client)
                print(f"Client removed : {client}")

class ConectionClient:
    def __init__(self):
        self.nickname = input("Choose your nickname : ").strip()
        while not self.nickname:
            self.nickname = input("Your nickname should not be empty : ").strip()
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost" # "127.0.1.1"
        self.port = 8000
        self.my_socket.connect((self.host, self.port))
        self.my_socket.setblocking(False)
        self.my_socket.send(f'@{self.nickname}'.encode())
        self.send_closed = False
    
    def start(self):
        thread_send = threading.Thread(target=self.thread_sending)
        thread_receive = threading.Thread(target=self.thread_receiving)
        thread_send.start()
        thread_receive.start()

    def thread_sending(self):
        self.send_closed
        while True:
            message_to_send = input()
            if message_to_send == 'close':
                self.my_socket.close()
                send_closed = False
                break
            if message_to_send:
                message_with_nickname = self.nickname + " : " + message_to_send
                self.my_socket.send(message_with_nickname.encode())
        
    def thread_receiving(self):
        while self.send_closed:
            message = self.my_socket.recv(1024).decode()
            print(message)
        

