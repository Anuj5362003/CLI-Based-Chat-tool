from base64 import encode
from tarfile import ENCODING
import threading
import socket

host="127.0.0.1"
port=55555
ENCODE="ascii"
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []    #new clients connecting to the server
nicknames = []  #inckname of the clients

def broadcast(message):     #broadcast message from server to all the clients including this server/client
    for client in clients:
        client.send(message)

def handle(client): #handling 1 client
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except: #client disconnects
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode(ENCODING))
            nicknames.remove(nickname)
            break
def receive():
    while True:
        client, address=server.accept()                         #loop waits here till server accepts connection request from client
        print(f"Connected with {str(address)}")
        client.send('NICK'.encode(ENCODING))
        nickname = client.recv(1024).decode(ENCODING)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f'{nickname} joined the chat'.encode(ENCODING))
        client.send('Connected to the server!'.encode(ENCODING))

        thread = threading.Thread(target=handle,args=(client,))     #one thread created for each client
        thread.start()
print("Server is listening....")
server_thread=threading.Thread(target=receive)
server_thread.start()
