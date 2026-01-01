import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {} 

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client):
    try:
        username = client.recv(1024).decode()
        clients[client] = username
        broadcast(f"{username} joined the chat.\n".encode(), client)

        while True:
            message = client.recv(1024)
            if not message:
                break
            full_message = f"{username}: {message.decode()}"
            broadcast(full_message.encode(), client)

    except:
        pass

    print(f"{clients[client]} disconnected")
    broadcast(f"{clients[client]} left the chat.\n".encode(), client)
    del clients[client]
    client.close()

print("Server running...")

while True:
    client, addr = server.accept()
    print(f"Connected with {addr}")
    threading.Thread(target=handle_client, args=(client,)).start()
