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

count_received=  0

while True:
    receivedPacket, adress = s.recvfrom(1094)
    fileNameLength, = struct.unpack("B", receivedPacket[0:1])
    fileName, = struct.unpack(f"{fileNameLength}s", receivedPacket[1:1+fileNameLength])
    flag,= struct.unpack("B", receivedPacket[1+fileNameLength : 2+fileNameLength])
    packet_number, = struct.unpack("4s", receivedPacket[2+fileNameLength : 6+fileNameLength])
    packet_number = int.from_bytes(packet_number, byteorder='big')
    dataSize = len(receivedPacket)
    dataSize = dataSize - 6 - fileNameLength
    fileData, = struct.unpack(f"{dataSize}s", receivedPacket[6+fileNameLength :])
    x=len(receivedPacket)
    # packet_number = receivedPacket[2+fileNameLength : 6+fileNameLength]
    fileName = fileName.decode("ascii")

    if flag == FIRST_PACKAGE:
        fileData = int.from_bytes(fileData, byteorder='big')
        logging.info(f"Recebendo arquivo {fileName} de tamanho {fileData} bytes")
        with open(f"./server_file/{fileName}", "xb") as f:
            f.close()
    
    #TODO Não está inserindo os bytes no arquivo corretamente
    if flag == PACKAGE_DATA:
        count_received += 1
        with open(f'./server_file/{fileName}', "r+b") as f:
            pos = (packet_number * FILE_DATA_SIZE)
            f.seek(pos)
            f.write(bytes(fileData))
            f.close()
    
    if flag == LAST_PACKAGE:
        fileChecksum = hashlib.sha1()
        with open(f'./server_file/{fileName}', 'rb') as f:
            while True:
                data = f.read(FILE_DATA_SIZE)
                if not data:
                    break
                fileChecksum.update(data)
            f.close()
        
        packed_response = None
        if fileChecksum.digest() != fileData:
            os.remove(f"./server_file/{fileName}")
            logging.info(f"Arquivo {fileName} corrompido, removendo")
            packed_response = struct.pack("B", UPLOAD_FAILED)
        else:
            logging.info(f"Arquivo {fileName} recebido com sucesso")
            packed_response = struct.pack("B", UPLOAD_SUCCESSFULL)

        s.sendto(packed_response, adress)
