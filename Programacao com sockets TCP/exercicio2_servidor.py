import socket, threading, hashlib, struct, os, logging
from tkinter import EXCEPTION
from exercicio2_status import *


log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def handleClient(con, client):
    Client(con, client)

class Client:
    def __init__(self, con, client):
        self.con = con
        self.client = client
        self.alive = True
        self.handleEvents()
        logging.info("Cliente desconectou")
        self.con.close()
        
    def response(self, command, status):
        packedResponse = struct.pack(
            "BBB",
            MESSAGE_TYPE_RESPONSE,
            command,
            status
        )
        self.con.send(packedResponse)    
    
    def handleEvents(self):
        while self.alive:
            msg = self.con.recv(3)
            if not msg:
                logging.info(f'Conexão com o cliente ({self.client}) encerrada')
                self.alive = False
                break
            type, command, filenameSize = struct.unpack('BBB', msg)
            filename = self.con.recv(filenameSize).decode('ascii')

            if type != MESSAGE_TYPE_REQUEST:
                continue

            try:
                if command == COMMAND_ADDFILE:
                    msg = self.con.recv(4)
                    fileSize, = struct.unpack('!I', msg)
                    fileData = bytes()
                    print(fileSize)
                    for i in range(fileSize):
                        fileData += (self.con.recv(1))
                    with open(f'./ex2_servidor_recebidos/{filename}', 'wb+') as f:
                        f.write(bytes(fileData))
                    self.response(command, STATUS_SUCCESS)
                    logging.info(f"Success on ADDFILE {filename}")
                
                if command == COMMAND_DELETE:
                    os.remove(f'./ex2_servidor_recebidos/{filename}')
                    self.response(command, STATUS_SUCCESS)
                    logging.info(f"Success on DELETE {filename}")
                
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
                            f'B{len(file)}s',
                            len(file),
                            bytes(file, 'ascii')
                        )
                        self.con.send(packedResponse)
                    logging.info(f'Success on GETFILESLIST')

                if command == COMMAND_GETFILE:
                    with open(f'./ex2_servidor_recebidos/{filename}', 'rb') as f:
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
                    logging.info(f"Success on GETFILE {filename}")           
            except Exception as e:
                logging.error(e)
                self.response(command, STATUS_ERROR)

HOST = ''              # Endereco IP do Servidor
PORT = 6666            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen()
while True:
    logging.info("Servidor aguardando conexão ...")
    con, cliente = tcp.accept()
    logging.info(f"Cliente ({cliente}) conectado --- Criando thread")
    client = threading.Thread(target=handleClient, args=(con, cliente,))
    client.start()