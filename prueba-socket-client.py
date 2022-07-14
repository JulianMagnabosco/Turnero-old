import sys
import socket
import threading
nickname = input("Choose your nickname : ").strip()
while not nickname:
    nickname = input("Your nickname should not be empty : ").strip()
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost" # "127.0.1.1"
port = 8000
my_socket.connect((host, port))
my_socket.send(f'@{nickname}'.encode())


send_closed = False
def thread_sending():
    global send_closed
    while True:
        message_to_send = input()
        if message_to_send == 'close':
            my_socket.close()
            send_closed = False
            break
        if message_to_send:
            message_with_nickname = nickname + " : " + message_to_send
            my_socket.send(message_with_nickname.encode())
        
def thread_receiving():
    while send_closed:
        message = my_socket.recv(1024).decode()
        print(message)
        
thread_send = threading.Thread(target=thread_sending)
thread_receive = threading.Thread(target=thread_receiving)
thread_send.start()
thread_receive.start()