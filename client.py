import socket
import os
import threading

HOST = '0.0.0.0'
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def handle_client(client_socket):
    with client_socket:
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



threading.Thread(target=handle_client, args=(client_socket,)).start()
if KeyboardInterrupt:
    client_socket.close()
