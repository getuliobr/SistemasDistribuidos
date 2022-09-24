"""
    Descrição: Arquivo de um Client para conexão com um servidor e envio de arquivos
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 19 / 09 / 2022
"""
import logging, hashlib,    sys
import socket, os, struct
import threading
from typing import Type
from ex2_utils import *
import time

# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
class Client:

    # Função para criar pacotes
    def sendHeader(self,fileName, flag, packet_number, dataSize, data):
        fileNameSize = len(fileName)
        fileName = bytes(fileName, 'ascii')
        packet_number = packet_number.to_bytes(4, byteorder='big')
        packed_request = struct.pack(f"B{fileNameSize}sB4s{dataSize}s"
                                    , fileNameSize
                                    , fileName
                                    , flag
                                    , packet_number
                                    , data
                                    )

        self.s.sendto(packed_request, (self.ip, self.portServer))

    # Função para receber input do usuário
    def userInput(self, needInput=1, filepath=""):
        
        uInput = ""
        # Se o upload vem da GUI, transforma o path em string
        if not needInput:
            uInput = "upload "+str(filepath)
        # Se vem do terminal, cria input
        else:
            uInput = input()

        # Separa o conteudo do input
        uInput = uInput.split(" ", 1)

        # Se o upload vem da GUI, separa o nome do arquivo relativo
        if not needInput:
            fileNameToServer = uInput[1].split("/")[-1]
        # Se vem do terminal, separa o nome do arquivo absoluto
        elif len(uInput) > 1:
            fileNameToServer = uInput[1]

        # Se o comando for pwd, retorna o diretório atual do client
        if uInput[0] == "pwd":
            print(os.getcwd().encode("utf-8"))

        # Se o comando for upload, envia o arquivo para o servidor
        if uInput[0] == "upload":
            # Se o arquivo existir, envia
            try:
                # Cria primeiro pacote com cabeçalho padrão e envia 
                fileSize = os.path.getsize(uInput[1])
                fileSizeToCount = fileSize
                fileSize = fileSize.to_bytes(4, byteorder='big')
                logging.info(f"Enviando arquivo {uInput[1]}")
                dataCounting = 0
                self.sendHeader(fileNameToServer, FIRST_PACKAGE, 34, 4, fileSize)

                # Abre o arquivo e envia os pacotes de dados
                with open(uInput[1], "rb") as f:
                    packet_number = 0
                    # Enquantos houver dados no arquivo, envia pacotes de dados com 1024 bytes de dados no máximo
                    while True:
                        data = f.read(FILE_DATA_SIZE)

                        if not data:
                            break
                        dataSize = len(data)
                        self.sendHeader(fileNameToServer, PACKAGE_DATA, packet_number, dataSize, data)
                        packet_number += 1

                        # Calcula o percentual de upload para a GUI
                        dataCounting += dataSize
                        self.percentage = (dataCounting/fileSizeToCount)*100

                        # Sleep necessário para não haver perca de pacotes no servidor
                        time.sleep(0.001)
                        
                    f.close()
                    # Seta a função de ativação do percentual para falso (GUI)
                    self.startedPercentage = False

                # Calcula o hash do arquivo enviado
                fileChecksum = hashlib.sha1()
                with open(uInput[1], "rb") as f:
                    while True:
                        data = f.read(FILE_DATA_SIZE)
                        if not data:
                            break
                        fileChecksum.update(data)
                    f.close()
                
                # Envia o último pacote com o hash do arquivo
                self.sendHeader(fileNameToServer, LAST_PACKAGE, packet_number, len(fileChecksum.digest()), fileChecksum.digest())
                logging.info("Arquivo enviado com sucesso")

            # Se o arquivo não existir, retorna erro
            except FileNotFoundError:
                logging.error(f"Arquivo {uInput[1]} não encontrado")

    # Função para receber pacotes do servidor
    def receiveThread(self):
        while self.running:
            # Recebe o pacote
            data, addr = self.s.recvfrom(1024)
            response, = struct.unpack(f"B", data[0:1])

            # Se o pacote for de confirmação de recebimento, imprime mensagem de sucesso no terminal e GUI
            if response == UPLOAD_SUCCESSFULL:
                self.uploadSuccessfull = True
                logging.info("Upload realizado com sucesso")

            # Se o pacote for de erro, imprime mensagem de erro no terminal e GUI
            if response == UPLOAD_FAILED:
                self.uploadSuccessfull = False
                logging.error("Upload falhou")

    def __init__(self):
        self.ip = "127.0.0.1" # IP do servidor
        self.portServer = 6001 # Porta do servidor
        self.portClient = 6000 # Porta do cliente
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria socket UDP
        self.s.bind((self.ip, self.portClient)) # Faz bind do socket com a porta do cliente
        logging.info("Cliente iniciado") 
        self.running=True # Variável para manter o cliente rodando
        self.percentage = 0 # Variável para armazenar o percentual de upload
        self.startedPercentage = True # Variável para ativar a função de percentual
        self.clientThread = threading.Thread(target=self.run).start() # Thread para enviar pacotes do servidor
        self.uploadSuccessfull = True # Variável para verificar se o upload foi bem sucedido
        self.receiveThread = threading.Thread(target=self.receiveThread).start() # Thread para receber pacotes do servidor
    
    # Função para rodar cliente pela GUI
    def runWithPath(self, filepath):
        self.userInput(0, filepath)

    # Função para rodar cliente pelo terminal
    def run(self):
        while self.running:
            self.userInput()