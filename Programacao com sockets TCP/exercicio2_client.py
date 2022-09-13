import logging
import socket, threading, os
import struct
from exercicio2_status import *

def handleClient(con):
    Client(con)

class Client:
    def __init__(self, con):
        self.con = con
        self.alive = True
        self.requestedFile = None
        self.send = threading.Thread(target=self.sendThread)
        self.send.start()
        self.receiveThread()
        print('Desconectado do servidor')
        self.con.close()
        
    def receiveThread(self):
        while self.alive:
            msg = (self.con.recv(1024))

            message_type, command, status = struct.unpack('BBB', msg[:3])
            if command == COMMAND_GETFILE:
                if status == STATUS_SUCCESS:
                    fileSize, = struct.unpack(f'!I', msg[3:])
                    fileData = bytes()
                    for i in range(fileSize):
                        fileData += (self.con.recv(1))
                    with open('./ex2_cliente_recebidos/' + self.requestedFile, 'wb+') as f:
                        f.write(bytes(fileData))          
                else:
                    self.requestedFile = None
                    logging.error("Erro ao receber o arquivo")

            if command == COMMAND_GETFILESLIST:
                if status == STATUS_SUCCESS:
                    print('Arquivos no servidor:')
                    files, = struct.unpack('!H', msg[3:])
                    for file in range(files):
                        fileReceived = self.con.recv(256)
                        filenameSize, = struct.unpack('B', fileReceived[:1])
                        filename = struct.unpack(f'255s', fileReceived[1:])
                        filename = filename[0].decode('ascii')
                        filename = filename[:filenameSize]
                        print(filename)
                else:
                    logging.error('Erro ao receber lista de arquivos')
            
            if command == COMMAND_ADDFILE:
                if status == STATUS_SUCCESS:
                    logging.info("Arquivo enviado com sucesso")
                else:
                    logging.error("Erro ao enviar arquivo")
            
            if command == COMMAND_DELETE:
                if status == STATUS_SUCCESS:
                    logging.info("Arquivo deletado com sucesso")
                else:
                    logging.error("Erro ao deletar arquivo")
            

    def sendThread(self):
        while self.alive:
            msg = input()
            msg = msg.split(' ')
            if msg[0] == 'ADDFILE' and msg[1] != '':
                try:
                    file = open(msg[1], 'rb')
                    data = file.read()
                    filesize = len(data)
                    filename = bytes(msg[1], 'ascii')
                    filenameSize = len(msg[1])
                    packedRequest = struct.pack(
                                        f'!BBB{filenameSize}sI', 
                                        MESSAGE_TYPE_REQUEST,
                                        COMMAND_ADDFILE,
                                        filenameSize,
                                        filename,
                                        filesize
                                        # data
                                    )
                    self.con.send(packedRequest)
                    for byteIndex in range(filesize):
                        self.con.send(struct.pack("B", data[byteIndex]))
                    file.close()
                except Exception as e:
                    logging.error("Erro ao adicionar arquivo", e)
            
            if msg[0] == 'GETFILESLIST':
                packedRequest = struct.pack(
                                    'BBBB', 
                                    MESSAGE_TYPE_REQUEST,
                                    COMMAND_GETFILESLIST,
                                    0x00,
                                    0x00
                                )
                self.con.send(packedRequest)
            
            if msg[0] == 'GETFILE':
                self.requestedFile = msg[1]
                filename = bytes(msg[1], 'ascii')
                filenameSize = len(msg[1])
                packedRequest = struct.pack(
                                    f'BBB{filenameSize}s', 
                                    MESSAGE_TYPE_REQUEST,
                                    COMMAND_GETFILE,
                                    filenameSize,
                                    filename
                                )
                self.con.send(packedRequest)
            
            if msg[0] == 'DELETE':
                filename = bytes(msg[1], 'ascii')
                filenameSize = len(msg[1])
                packedRequest = struct.pack(
                                    f'BBB{filenameSize}s', 
                                    MESSAGE_TYPE_REQUEST,
                                    COMMAND_DELETE,
                                    filenameSize,
                                    filename
                                )
                self.con.send(packedRequest)

            if msg[0] == 'PWD':
                print(os.getcwd().encode("utf-8"))

            if not self.alive:
                break
            # self.con.send(msg.encode())
            if msg == 'PARAR':
                self.alive = False
                break


HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 6666            # Porta que o Servidor esta
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
con.connect(dest)

receive = threading.Thread(target=handleClient, args=(con,))
receive.start()
