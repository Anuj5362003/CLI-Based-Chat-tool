from tarfile import ENCODING
import threading
import socket

nickname=input("Enter nickname : ")

ENCODING="ascii"
client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    while True:
        try:
            message=client.recv(1024).decode(ENCODING)
            if message == 'NICK':
                client.send(nickname.encode(ENCODING))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break
def write():
    while True:
        message= f'{nickname}:{input("")}'
        client.send(message.encode(ENCODING))
        
receive_thread=threading.Thread(target=receive)
receive_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()
