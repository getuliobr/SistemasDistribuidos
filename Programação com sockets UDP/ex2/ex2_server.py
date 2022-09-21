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
    #TODO arrumar pacote, por algum motivo não tá empacotando o tamanho correto
    receivedPacket, adress = s.recvfrom(1094)
    fileNameLength, = struct.unpack("B", receivedPacket[0:1])
    fileName, = struct.unpack(f"{fileNameLength}s", receivedPacket[1:1+fileNameLength])
    flag,= struct.unpack("B", receivedPacket[1+fileNameLength : 2+fileNameLength])
    packet_number, = struct.unpack("I", receivedPacket[2+fileNameLength : 6+fileNameLength])
    dataSize, = struct.unpack("H", receivedPacket[6+fileNameLength : 8+fileNameLength])
    # fileData = struct.unpack(f"{dataSize}s", receivedPacket[5+fileNameLength:])

    if flag == FIRST_PACKAGE:
        logging.info(f"Recebendo arquivo {fileName} de tamanho {fileData} bytes")
        with open(f"./server_file/{fileName}", "xb") as f:
            f.close()
    
    if flag == PACKAGE_DATA:
        with open(fileName, "ab") as f:
            f.seek(FILE_DATA_SIZE * packet_number)
            f.write(fileData)
            f.close()
    
    if flag == LAST_PACKAGE:
        fileChecksum = hashlib.sha1()
        with open(fileName, 'rb') as f:
            while True:
                data = f.read(FILE_DATA_SIZE)
                if not data:
                    break
                fileChecksum.update(data)
            f.close()
        if fileChecksum.digest() != fileData:
            os.remove(f"./server_file/{fileName}")
            logging.info(f"Arquivo {fileName} corrompido, removendo")
        else:
            logging.info(f"Arquivo {fileName} recebido com sucesso")

