import logging
import socket, threading, os
import struct
from exercicio2_status import *

# Método que cria um cliente
def handleClient(con):
    Client(con)

# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# Classe que representa um cliente
class Client:
    def __init__(self, con):
        self.con = con
        self.alive = True
        self.requestedFile = None
        self.send = threading.Thread(target=self.sendThread) # Thread para enviar mensagens
        self.send.start() # Inicia a thread de envio
        self.receiveThread() # Inicia a thread de recebimento
        print('Desconectado do servidor')
        self.con.close()

    # Thread que recebe mensagens    
    def receiveThread(self):
        while self.alive:
            # Recebe response com cabeçalho comum
            msg = self.con.recv(3)
            message_type, command, status = struct.unpack('BBB', msg)

            # Se a response possuir comando GETFILE
            if command == COMMAND_GETFILE:
                # Caso Sucesso
                if status == STATUS_SUCCESS:
                    # Desempacota tamanho do arquivo (2 bytes)
                    fileSize, = struct.unpack(f'!I', self.con.recv(4))
                    fileData = bytes()
                    logging.info(f"Fazendo download arquivo de {fileSize} bytes")

                    # Abre o arquivo na pasta de recebimento do cliente e escreve os bytes recebidos 1 por 1
                    with open('./ex2_cliente_recebidos/' + self.requestedFile, 'wb') as file:
                        for i in range(fileSize):
                            file.write(bytes(self.con.recv(1)))      
                    logging.info("Arquivo recebido com sucesso") 
                
                # Caso Erro imprime mensagem de erro
                else:
                    self.requestedFile = None
                    logging.error("Erro ao receber o arquivo")
            
            # Se a response possuir comando GETFILESLIST
            if command == COMMAND_GETFILESLIST:
                # Caso Sucesso
                if status == STATUS_SUCCESS:
                    # Desempacota a quantidade de arquivos a serem recebidos (2 bytes)
                    filesAmount, = struct.unpack('!H', self.con.recv(2))
                    if(filesAmount == 0):
                        logging.info("Nenhum arquivo no servidor")
                        continue

                    logging.info(f'{filesAmount} arquivos no servidor:')
                    # Recebe os nomes dos arquivos um por um
                    for i in range(filesAmount):
                        filenameSize, = struct.unpack('B', self.con.recv(1))
                        filename = self.con.recv(filenameSize).decode('ascii')
                        print('-' + filename)

                # Caso Erro imprime mensagem de erro
                else:
                    logging.error('Erro ao receber lista de arquivos')
            
            # Caso a response possuir comando ADDFILE
            if command == COMMAND_ADDFILE:
                # Caso Sucesso imprime mensagem de sucesso
                if status == STATUS_SUCCESS:
                    logging.info("Arquivo enviado com sucesso")
                # Caso Erro imprime mensagem de erro
                else:
                    logging.error("Erro ao enviar arquivo")
            
            # Caso a response possuir comando DELETE
            if command == COMMAND_DELETE:
                # Caso Sucesso imprime mensagem de sucesso
                if status == STATUS_SUCCESS:
                    logging.info("Arquivo deletado com sucesso")
                # Caso Erro imprime mensagem de erro
                else:
                    logging.error("Erro ao deletar arquivo")
            
    # Thread que envia mensagens
    def sendThread(self):
        while self.alive:
            msg = input()
            msg = msg.split(' ')
            # Se o comando for ADDFILE
            if msg[0] == 'ADDFILE' and msg[1] != '':
                try:
                    # Abre o arquivo na pasta de envio do cliente
                    file = open(msg[1], 'rb')
                    data = file.read()
                    filesize = len(data)
                    logging.info(f"Bytes a serem enviados: {filesize}")
                    filename = bytes(msg[1], 'ascii')
                    filenameSize = len(msg[1])

                    # Empacota o request em um cabeçalho comum com tamanho do arquivo e envia
                    packedRequest = struct.pack(
                                        f'!BBB{filenameSize}sI', 
                                        MESSAGE_TYPE_REQUEST,
                                        COMMAND_ADDFILE,
                                        filenameSize,
                                        filename,
                                        filesize
                                    )
                    self.con.send(packedRequest)

                    # Envia os bytes do arquivo um por um
                    for byteIndex in range(filesize):
                        self.con.send(struct.pack("B", data[byteIndex]))
                    file.close()

                # Caso algum erro ocorra, imprime mensagem de erro
                except Exception as e:
                    logging.error("Erro ao adicionar arquivo", e)
            
            # Se o comando for GETFILESLIST
            if msg[0] == 'GETFILESLIST':
                # Empacota o request em um cabeçalho comum e envia
                packedRequest = struct.pack(
                                    'BBBB', 
                                    MESSAGE_TYPE_REQUEST,
                                    COMMAND_GETFILESLIST,
                                    0x01,
                                    0x01
                                )
                self.con.send(packedRequest)
            
            # Se o comando for GETFILE
            if msg[0] == 'GETFILE':
                self.requestedFile = msg[1]
                filename = bytes(msg[1], 'ascii')
                filenameSize = len(msg[1])
                # Empacota o request em um cabeçalho comum com o nome do arquivo e envia
                packedRequest = struct.pack(
                                    f'BBB{filenameSize}s', 
                                    MESSAGE_TYPE_REQUEST,
                                    COMMAND_GETFILE,
                                    filenameSize,
                                    filename
                                )
                self.con.send(packedRequest)
            
            # Se o comando for DELETE
            if msg[0] == 'DELETE':
                filename = bytes(msg[1], 'ascii')
                filenameSize = len(msg[1])
                # Empacota o request em um cabeçalho comum com o nome do arquivo e envia
                packedRequest = struct.pack(
                                    f'BBB{filenameSize}s', 
                                    MESSAGE_TYPE_REQUEST,
                                    COMMAND_DELETE,
                                    filenameSize,
                                    filename
                                )
                self.con.send(packedRequest)

            # Se o comando for PWD, imprime o diretório atual
            if msg[0] == 'PWD':
                print(os.getcwd().encode("utf-8"))


            if not self.alive:
                break

            # Se o comando for PARAR, encerra a conexão
            if msg == 'PARAR':
                self.alive = False
                break


HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 6666            # Porta que o Servidor esta
con = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket TCP
dest = (HOST, PORT) # Define o destino
con.connect(dest) # Conecta ao servidor

receive = threading.Thread(target=handleClient, args=(con,)) # Cria uma thread de Cliente
receive.start() # Inicia a thread de Cliente 
