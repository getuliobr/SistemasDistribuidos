"""
    Descrição: Servidor para listagem e transferência de arquivos com protocolo em binário
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 12 / 09 / 2022
"""

import socket, threading, struct, os, logging
from exercicio2_utils import convertBytesNumber
from exercicio2_utils import *


# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# Método que cria um cliente
def handleClient(con, client):
    Client(con, client)

# Classe que representa um cliente
class Client:
    def __init__(self, con, client):
        self.con = con
        self.client = client
        self.alive = True
        self.handleEvents() # Inicia a thread
        logging.info("Cliente desconectou")
        self.con.close()
        
    def response(self, command, status):
        # Empacota a resposta com cabeçalho comum e envia
        packedResponse = struct.pack(
            "BBB",
            MESSAGE_TYPE_RESPONSE,
            command,
            status
        )
        self.con.send(packedResponse)    
    
    def handleEvents(self):
        while self.alive:
            # Recebe os 3 primeimros bytes cabeçalho da mensagem contendo informações sobre o comando
            msg = self.con.recv(3)
            if not msg: # Se a mensagem for vazia, o cliente desconectou
                logging.info(f'Conexão com o cliente ({self.client}) encerrada')
                self.alive = False
                break
            type, command, filenameSize = struct.unpack('BBB', msg)

            # Recebe o nome do arquivo
            filename = self.con.recv(filenameSize).decode('ascii')

            if type != MESSAGE_TYPE_REQUEST:
                continue

            try:
                # Se o comando for ADDFILE
                if command == COMMAND_ADDFILE:
                    msg = self.con.recv(4) # Recebe os atributos do arquivo
                    fileSize, = struct.unpack('!I', msg)
                    fileData = bytes()
                    logging.info(f'Arquivo {filename} de tamanho {convertBytesNumber(fileSize)} sendo recebido do cliente ({self.client})')

                    # Cria o arquivo e recebe os bytes do cliente
                    with open(f'./ex2_servidor_recebidos/{filename}', 'wb') as file:
                        for i in range(fileSize):
                            file.write(bytes(self.con.recv(1)))

                    # Responde ao cliente com sucesso
                    self.response(command, STATUS_SUCCESS)
                    logging.info(f"Success on ADDFILE {filename}")
                
                # Se o comando for DELETE
                if command == COMMAND_DELETE:
                    # Se o arquivo existir, deleta e responde com sucesso
                    os.remove(f'./ex2_servidor_recebidos/{filename}')
                    self.response(command, STATUS_SUCCESS)
                    logging.info(f"Success on DELETE {filename}")
                
                # Se o comando for GETFILESLIST
                if command == COMMAND_GETFILESLIST:
                    # Lista os arquivos do diretório
                    files = os.listdir('./ex2_servidor_recebidos')
                    # Empacota response com cabeçalho comum e quantidade de arquivos, e envia
                    packedResponse = struct.pack(
                        f'!BBBH',
                        MESSAGE_TYPE_RESPONSE,
                        COMMAND_GETFILESLIST,
                        STATUS_SUCCESS,
                        len(files)
                    )
                    self.con.send(packedResponse)

                    # Para cada arquivo, empacota o tamanho do nome e nome e envia
                    for file in files:
                        packedResponse = struct.pack(
                            f'B{len(file)}s',
                            len(file),
                            bytes(file, 'ascii')
                        )
                        self.con.send(packedResponse)
                    logging.info(f'Success on GETFILESLIST')

                # Se o comando for GETFILE
                if command == COMMAND_GETFILE:
                    # Se o arquivo existir, lê o arquivo
                    with open(f'./ex2_servidor_recebidos/{filename}', 'rb') as f:
                        data = f.read()
                    fileSize = len(data)
                    logging.info(f'Arquivo {filename} de tamanho {convertBytesNumber(fileSize)} sendo enviado para o cliente ({self.client})')
                    # Empacota response com cabeçalho comum e tamanho do arquivo, e envia
                    packedResponse = struct.pack(
                        f'!BBBI',
                        MESSAGE_TYPE_RESPONSE,
                        COMMAND_GETFILE,
                        STATUS_SUCCESS,
                        fileSize
                    )
                    self.con.send(packedResponse)

                    # Para cada byte do arquivo, envia
                    for byteIndex in range(fileSize):
                        self.con.send(struct.pack("B", data[byteIndex]))
                    logging.info(f"Success on GETFILE {filename}")      

            # Caso ocorra algum erro, responde com erro     
            except Exception as e:
                logging.error(e)
                self.response(command, STATUS_ERROR)

HOST = ''              # Endereco IP do Servidor
PORT = 6666            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket TCP
orig = (HOST, PORT) # Define o endereço do servidor
tcp.bind(orig) # Associa o socket ao endereço
tcp.listen() # Coloca o socket em modo de escuta
while True:
    logging.info("Servidor aguardando conexão ...")
    con, cliente = tcp.accept() # Espera uma conexão
    logging.info(f"Cliente ({cliente}) conectado --- Criando thread")
    client = threading.Thread(target=handleClient, args=(con, cliente,)) # Cria uma thread para o cliente
    client.start()