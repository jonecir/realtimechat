import socket
import threading

HOST = 'localhost'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

chatrooms = {}


def sendMessage(user, room, client):
    while True:
        msg = client.recv(1024)
        msg = f"{user}: {msg.decode()}\n"
        broadcast(room, msg)


def broadcast(room, msg):
    for r in chatrooms[room]:
        if isinstance(msg, str):
            msg = msg.encode()
        
        r.send(msg)


while True:
    client, addr = server.accept()
    client.send(b'ROOM')
    room = client.recv(1024).decode()
    user = client.recv(1024).decode()
    if (room not in chatrooms.keys()):
        chatrooms[room] = []
    
    chatrooms[room].append(client)
    #print(f'{user} just joined in the {room} room! INFO {addr}\n')
    broadcast(room, f'{user} just joined the chatroom!\n')
    
    thread = threading.Thread(target=sendMessage, args=(user, room, client))
    thread.start()
    
