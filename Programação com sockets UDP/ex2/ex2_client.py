import logging, hashlib,    sys
import socket, os, struct
import threading
from typing import Type
from ex2_utils import *
import time

# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
class Client:

    

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

    def userInput(self, needInput=1, filepath=""):
        
        
        uInput = ""
        if not needInput:
            uInput = "upload "+str(filepath)
        else:
            uInput = input()

        uInput = uInput.split(" ", 1)

        if not needInput:
            fileNameToServer = uInput[1].split("/")[-1]
        else:
            fileNameToServer = uInput[1]

        if uInput[0] == "pwd":
            print(os.getcwd().encode("utf-8"))

        if uInput[0] == "upload":
            try:
                #TODO Arrumar filesize do primeiro pacote
                fileSize = os.path.getsize(uInput[1])
                fileSizeToCount = fileSize
                fileSize = fileSize.to_bytes(4, byteorder='big')
                logging.info(f"Enviando arquivo {uInput[1]}")
                dataCounting = 0
                self.sendHeader(fileNameToServer, FIRST_PACKAGE, 34, 4, fileSize)
                with open(uInput[1], "rb") as f:
                    packet_number = 0
                    while True:
                        data = f.read(FILE_DATA_SIZE)

                        if not data:
                            break
                        dataSize = len(data)
                        dataCounting += dataSize
                        self.sendHeader(fileNameToServer, PACKAGE_DATA, packet_number, dataSize, data)
                        packet_number += 1
                        self.percentage = (dataCounting/fileSizeToCount)*100
                        time.sleep(0.001)
                        
                    f.close()
                    self.startedPercentage = False

                fileChecksum = hashlib.sha1()
                with open(uInput[1], "rb") as f:
                    while True:
                        data = f.read(FILE_DATA_SIZE)
                        if not data:
                            break
                        fileChecksum.update(data)
                    f.close()
                self.sendHeader(fileNameToServer, LAST_PACKAGE, packet_number, len(fileChecksum.digest()), fileChecksum.digest())
                logging.info("Arquivo enviado com sucesso")

                    
            except FileNotFoundError:
                logging.error(f"Arquivo {uInput[1]} não encontrado")

    def receiveThread(self):
        while self.running:
            data, addr = self.s.recvfrom(1024)
            response, = struct.unpack(f"B", data[0:1])
            if response == UPLOAD_SUCCESSFULL:
                self.uploadSuccessfull = True
                logging.info("Upload realizado com sucesso")
            if response == UPLOAD_FAILED:
                self.uploadSuccessfull = False
                logging.error("Upload falhou")

    def __init__(self):
        self.ip = "127.0.0.1"
        self.portServer = 6001
        self.portClient = 6000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.ip, self.portClient))
        logging.info("Cliente iniciado")
        self.running=True
        self.percentage = 0
        self.startedPercentage = True
        self.clientThread = threading.Thread(target=self.run).start()
        self.uploadSuccessfull = True
        self.receiveThread = threading.Thread(target=self.receiveThread).start()
    
    def runWithPath(self, filepath):
        self.userInput(0, filepath)

    def run(self):
        pass
        while self.running:
            self.userInput()