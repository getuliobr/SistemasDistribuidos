import logging, hashlib,    sys
import socket, os, struct
from typing import Type
from ex2_utils import *

# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

ip = "127.0.0.1"
portServer = 6001
portClient = 6000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, portClient))
logging.info("Cliente iniciado")

def sendHeader(fileName, flag, packet_number, dataSize, data):
    fileNameSize = len(fileName)
    fileName = bytes(fileName, 'ascii')
    print(f"Data = {dataSize}")
    packed_request = struct.pack(f"B{fileNameSize}sBIH"
                                , len(fileName)
                                , fileName
                                , flag
                                , packet_number
                                , dataSize
                                )
    print(len(packed_request))
    s.sendto(packed_request, (ip, portServer))

def userInput():
    uInput = input().split(" ", 1)
    
    if uInput[0] == "pwd":
        print(os.getcwd().encode("utf-8"))

    if uInput[0] == "upload":
        try:
            #TODO Arrumar filesize do primeiro pacote
            fileSize = os.path.getsize(uInput[1])
            fileSize = fileSize.to_bytes(4, byteorder='big')
            logging.info(f"Enviando arquivo {uInput[1]}")
            sendHeader(uInput[1], FIRST_PACKAGE, 0, 4, fileSize)
            with open(uInput[1], "rb") as f:
                packet_number = 0
                while True:
                    data = f.read(FILE_DATA_SIZE)

                    if not data:
                        break
                    dataSize = len(data)
                    sendHeader(uInput[1], PACKAGE_DATA, packet_number, dataSize, data)
                    packet_number += 1
                f.close()
            fileChecksum = hashlib.sha1()
            with open(uInput[1], "rb") as f:
                while True:
                    data = f.read(FILE_DATA_SIZE)
                    if not data:
                        break
                    fileChecksum.update(data)
                f.close()
            sendHeader(uInput[1], LAST_PACKAGE, packet_number, len(fileChecksum.digest()), fileChecksum.digest())
            logging.info("Arquivo enviado com sucesso")

                
        except FileNotFoundError:
            logging.error(f"Arquivo {uInput[1]} não encontrado")

while True:
    userInput()