# Goal: 1-1 File transfer over TCP/IP in CLI, based on the
# provided chat system
# • One server
# • One client
# • Using socket
# • Write a short report in LATEX:
# • Name it « 01.tcp.file.transfer.tex »
# • How you design your protocol. Figure.
# • How you organize your system. Figure.
# • How you implement the file transfer. Code snippet.

import socket
import os
import threading


HOST = '0.0.0.0'
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

def handle_client(client_socket):
        print("Available files:")
        list_of_files = os.listdir('.')
        for idx, file in enumerate(list_of_files):
            print(f"{idx}: {file}")
        file_index = int(input("Enter the index of the file to send: "))
        filename = list_of_files[file_index]
        client_socket.sendall(filename.encode())
        print(f"Sending file: {filename}")
        with open(filename, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                client_socket.sendall(data)
        print(f"File {filename} sent successfully.")

while True:
    cSocket, cAddr = server_socket.accept()
    print(f"Connection from {cAddr}")




    threading.Thread(target=handle_client, args=(cSocket,)).start()

        