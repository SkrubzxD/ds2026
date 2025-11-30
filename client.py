import socket
import os
import threading

HOST = '0.0.0.0'
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def request(client_socket):
    welcome_msg = client_socket.recv(1024).decode()
    print(welcome_msg)
    while True:
        command = input("sftp> ")
        client_socket.sendall(command.encode())
        
        
#Main
try:    
    threading.Thread(target=request, args=(client_socket,)).start()
except KeyboardInterrupt:
        client_socket.close()   
        quit()