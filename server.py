import socket
import os
import threading

#Definitions
HOST = '0.0.0.0'
PORT = 5001

#Call Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

def commandHandler(command, client_socket):
        msg = ""
        if command == "ls":
            files = os.listdir('.')
            msg += "Files in directory:\n"
            for f in files:
                msg += f + "\n"
        if command.startswith("get "):
            filename = command[4:]
            if os.path.isfile(filename):
                with open(filename, 'rb') as f:
                    data = f.read()
                    client_socket.sendall(data)
                msg += f"File {filename} sent successfully.\n"
            else:
                msg += f"File not found: {filename}\n"
        if command == "quit":
            msg += "Connection closed by server.\n"
            client_socket.close()
        else:
            msg += "Invalid command.\n"
        client_socket.sendall(msg.encode())

def handle_client(client_socket):
    client_socket.send(b"Welcome to the File Server!\n")
    while True:
        command = client_socket.recv(1024).decode()
        commandHandler(command, client_socket)
#Main
try:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()
except BrokenPipeError:
        print("Client disconnected")

