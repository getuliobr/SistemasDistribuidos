"""
    Descrição: Servidor para listagem e transferência de arquivos com protocolo em binário
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 12 / 09 / 2022
"""

import socket, threading, struct, os, logging
import ProtoFiles.matricula_pb2 as matricula_pb2

from server_utils import CLASS_MATRICULA, COMMAND_CREATE


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
        
    
    def handleEvents(self):
        while self.alive:
            # Recebe o primeiro byte do cabeçalho da mensagem contendo informações sobre o comando
            command = self.con.recv(1)
            command = struct.unpack('B', command)[0]

            if not command:
                break
            
            if command == COMMAND_CREATE:
                print("Recebeu comando de criação")
                type = self.con.recv(1)
                type = struct.unpack('B', type)[0]
                print(type)
                sizeType = self.con.recv(4)
                sizeType = struct.unpack('I', sizeType)[0]
                print(type, sizeType)
                if type == CLASS_MATRICULA:
                    data = self.con.recv(sizeType)
                    matricula = matricula_pb2.Matricula()
                    matricula.ParseFromString(data)
                    print(matricula)

            

HOST = ''              # Endereco IP do Servidor
PORT = 6666            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket TCP
orig = (HOST, PORT) # Define o endereço do servidor
tcp.bind(orig) # Associa o socket ao endereço
tcp.listen() # Coloca o socket em modo de escuta
while True:
    try:
        logging.info("Servidor aguardando conexão ...")
        con, cliente = tcp.accept() # Espera uma conexão
        logging.info(f"Cliente ({cliente}) conectado --- Criando thread")
        client = threading.Thread(target=handleClient, args=(con, cliente,)) # Cria uma thread para o cliente
        client.start()
    except KeyboardInterrupt:
        print("Servidor encerrado")
        break