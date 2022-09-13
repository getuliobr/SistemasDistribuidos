import socket, threading, hashlib, struct, os
from tkinter import EXCEPTION
from exercicio2_status import *

def handleClient(con):
    Client(con)

class Client:
    def __init__(self, con):
        self.con = con
        self.alive = True
        self.send = threading.Thread(target=self.sendThread)
        self.send.start()
        self.receiveThread()
        print('Cliente desconectou')
        self.con.close()
        
    def response(self, command, status):
        packedResponse = struct.pack(
            "BBB",
            MESSAGE_TYPE_RESPONSE,
            command,
            status
        )
        self.con.send(packedResponse)    
    
    def receiveThread(self):
        while self.alive:
            msg = (self.con.recv(1024))
            type, command, filenameSize = struct.unpack('BBB', msg[:3])
            if type != MESSAGE_TYPE_REQUEST:
                continue
            try:
                if command == COMMAND_ADDFILE:
                    filename, fileSize = struct.unpack(f'!{filenameSize}sI', msg[3:])
                    print(filename, fileSize)
                    fileData = bytes()
                    for i in range(fileSize):
                        fileData += (self.con.recv(1))
                    with open('./ex2_servidor_recebidos/' + filename.decode('ascii'), 'wb+') as f:
                        f.write(bytes(fileData))
                    self.response(command, STATUS_SUCCESS)
                
                if command == COMMAND_DELETE:
                    filename, = struct.unpack(f'!{filenameSize}s', msg[3:])
                    os.remove('./ex2_servidor_recebidos/' + filename.decode('ascii'))
                    self.response(command, STATUS_SUCCESS)
                
                if command == COMMAND_GETFILESLIST:
                    files = os.listdir('./ex2_servidor_recebidos')
                    packedResponse = struct.pack(
                        f'!BBBH',
                        MESSAGE_TYPE_RESPONSE,
                        COMMAND_GETFILESLIST,
                        STATUS_SUCCESS,
                        len(files)
                    )
                    self.con.send(packedResponse)
                    for file in files:
                        packedResponse = struct.pack(
                            f'B255s',
                            len(file),
                            bytes(file, 'ascii')
                        )
                        self.con.send(packedResponse)

                if command == COMMAND_GETFILE:
                    filename, = struct.unpack(f'!{filenameSize}s', msg[3:])
                    with open('./ex2_servidor_recebidos/' + filename.decode('ascii'), 'rb') as f:
                        data = f.read()
                    fileSize = len(data)
                    packedResponse = struct.pack(
                        f'!BBBI',
                        MESSAGE_TYPE_RESPONSE,
                        COMMAND_GETFILE,
                        STATUS_SUCCESS,
                        fileSize
                    )
                    self.con.send(packedResponse)
                    for byteIndex in range(fileSize):
                        self.con.send(struct.pack("B", data[byteIndex]))
                    f.close()
                
            except Exception as e:
                print(e)
                self.response(command, STATUS_ERROR)

    def sendThread(self):
        while self.alive:
            msg = input()
            if not self.alive:
                break
            self.con.send(msg.encode())
            if msg == 'PARAR':
                self.alive = False
                break

HOST = ''              # Endereco IP do Servidor
PORT = 6666            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
while True:
    print("Servidor aguardando conexao ...")
    con, cliente = tcp.accept()
    print("Cliente conectado ... Criando thread ...");
    client = threading.Thread(target=handleClient, args=(con,))
    client.start()