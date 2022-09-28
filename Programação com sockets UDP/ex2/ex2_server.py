"""
    Descrição: Arquivo de um Servidor que recebe arquivos
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 19 / 09 / 2022
"""
import socket, threading, os, struct, logging
from ex2_utils import *
import sys
import hashlib

# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# Define IP e porta do servidor
ip = "127.0.0.1"
port = 6001

# Cria um socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))
logging.info(f"Servidor iniciado na porta {port}")

# Variavel de verificação de continuação de recebimento de pacotes
canSave = 1

# Função que recebe os dados do cliente
while True:
    # Recebe os dados do cliente e desempacota
    receivedPacket, adress = s.recvfrom(1094)
    fileNameLength, = struct.unpack("B", receivedPacket[0:1])
    fileName, = struct.unpack(f"{fileNameLength}s", receivedPacket[1:1+fileNameLength])
    flag,= struct.unpack("B", receivedPacket[1+fileNameLength : 2+fileNameLength])
    packet_number, = struct.unpack("4s", receivedPacket[2+fileNameLength : 6+fileNameLength])
    packet_number = int.from_bytes(packet_number, byteorder='big')
    dataSize = len(receivedPacket)
    dataSize = dataSize - 6 - fileNameLength
    fileData, = struct.unpack(f"{dataSize}s", receivedPacket[6+fileNameLength :])
    fileName = fileName.decode("ascii")

    # Se for o primeiro pacote, verifica se o arquivo já existe, se não existir, cria o arquivo
    if flag == FIRST_PACKAGE:
        # Se o arquivo não existir, cria o arquivo e seta a variavel de verificação para continuar recebendo pacotes
        try:
            fileData = int.from_bytes(fileData, byteorder='big')
            logging.info(f"Recebendo arquivo {fileName} do ip {adress} de tamanho {convertBytesNumber(fileData)}")
            with open(f"./server_file/{fileName}", "xb") as f:
                f.close()
            canSave = 1
        # Se o arquivo já existir, seta a variavel de verificação para não continuar recebendo pacotes
        except FileExistsError:
            logging.info(f"Arquivo {fileName} já existe")
            packed_response = struct.pack("B", UPLOAD_FAILED)
            s.sendto(packed_response, adress)
            canSave = 0

    # Escreve os dados no arquivo
    if flag == PACKAGE_DATA and canSave:
        with open(f'./server_file/{fileName}', "r+b") as f:
            pos = (packet_number * FILE_DATA_SIZE)
            f.seek(pos)
            f.write(bytes(fileData))
            f.close()
    
    # Se for o último pacote, verifica se o arquivo foi recebido corretamente
    if flag == LAST_PACKAGE and canSave:
        # Calcula o hash do arquivo recebido no servidor
        fileChecksum = hashlib.sha1()
        with open(f'./server_file/{fileName}', 'rb') as f:
            while True:
                data = f.read(FILE_DATA_SIZE)
                if not data:
                    break
                fileChecksum.update(data)
            f.close()
        
        packed_response = None
        # Verifica se o hash do arquivo recebido é igual ao hash do arquivo enviado
        if fileChecksum.digest() != fileData:
            os.remove(f"./server_file/{fileName}")
            logging.info(f"Arquivo {fileName} corrompido, removendo")
            packed_response = struct.pack("B", UPLOAD_FAILED)
        else:
            logging.info(f"Arquivo {fileName} recebido com sucesso")
            packed_response = struct.pack("B", UPLOAD_SUCCESSFULL)

        # Envia a resposta para o cliente
        s.sendto(packed_response, adress)
