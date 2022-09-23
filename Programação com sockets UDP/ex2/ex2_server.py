import socket, threading, os, struct, logging
from ex2_utils import *

import sys
import hashlib

# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


ip = "127.0.0.1"
port = 6001

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))
logging.info(f"Servidor iniciado na porta {port}")

while True:
    receivedPacket, adress = s.recvfrom(1094)
    fileNameLength, = struct.unpack("B", receivedPacket[0:1])
    fileName, = struct.unpack(f"{fileNameLength}s", receivedPacket[1:1+fileNameLength])
    flag,= struct.unpack("B", receivedPacket[1+fileNameLength : 2+fileNameLength])
    packet_number, = struct.unpack("I", receivedPacket[2+fileNameLength : 6+fileNameLength])
    dataSize = len(receivedPacket)-(1+fileNameLength+1+4)-1
    fileData, = struct.unpack(f"{dataSize}s", receivedPacket[7+fileNameLength :])

    fileName = fileName.decode("ascii")

    if flag == FIRST_PACKAGE:
        fileData = int.from_bytes(fileData, byteorder='big')
        logging.info(f"Recebendo arquivo {fileName} de tamanho {fileData} bytes")
        with open(f"./server_file/{fileName}", "xb") as f:
            f.close()
    
    #TODO Não está inserindo os bytes no arquivo
    if flag == PACKAGE_DATA:
        with open(fileName, "rb+") as f:
            f.seek(FILE_DATA_SIZE * (packet_number+1))
            f.write(fileData)
            f.close()
    
    if flag == LAST_PACKAGE:
        pass
        # fileChecksum = hashlib.sha1()
        # with open(fileName, 'rb') as f:
        #     while True:
        #         data = f.read(FILE_DATA_SIZE)
        #         if not data:
        #             break
        #         fileChecksum.update(data)
        #     f.close()
        # if fileChecksum.digest() != fileData:
        #     os.remove(f"./server_file/{fileName}")
        #     logging.info(f"Arquivo {fileName} corrompido, removendo")
        # else:
        #     logging.info(f"Arquivo {fileName} recebido com sucesso")

