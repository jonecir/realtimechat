import socket
import threading
import tkinter
from tkinter import *
from tkinter import simpledialog


class Chat:
    def __init__(self):
        HOST = 'localhost'
        PORT = 55555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        login = Tk()
        login.withdraw()

        self.loaded_window = False
        self.active = True

        self.user = simpledialog.askstring('User', 'Enter your name:', parent=login)
        self.room = simpledialog.askstring('Room', 'Enter room name:', parent=login)
        
        thread = threading.Thread(target=self.conectar)
        thread.start()
    
        self.window()


    def conectar(self):
        while True:
            recvMsg = self.client.recv(1024)
            if (recvMsg == b'ROOM'):
                self.client.send(self.room.encode())
                self.client.send(self.user.encode())
            else:
                try:
                    self.text_box.insert("end",recvMsg.decode())
                except:
                    pass


    def submitMessage(self):
        msg = self.sendMsg.get()
        self.client.send(msg.encode())


    def closeWindow(self):
        self.root.destroy()
        self.client.close()


    def window(self):
        self.root = Tk()
        self.root.geometry("600x500")
        self.root.title('Simple Chat App')

        self.text_box = Text(self.root)
        self.text_box.place(relx=0.05, rely=0.01, width=540, height=400)
        
        self.sendMsg = Entry(self.root)
        self.sendMsg.place(relx=0.05, rely=0.85, width=350, height=25)

        self.btnSubmit = Button(self.root, text="Submit", command=self.submitMessage)
        self.btnSubmit.place(relx=0.7, rely=0.85, width=80, height=25)
        
        self.root.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.root.mainloop()


chat = Chat()

