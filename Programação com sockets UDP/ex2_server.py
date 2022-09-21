import socket, threading, os, struct, logging
from ex2_utils import *

import sys
import hashlib

# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


ip = "127.0.0.1"
port = 6001

s = socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(ip, port)

while True:
    receivedPacket, adress = s.recvfrom(1094)
    fileNameLength = struct.unpack("B", receivedPacket[0:1])
    fileName = struct.unpack(f"{fileNameLength}s", receivedPacket[1:1+fileNameLength])
    flag, packet_number = struct.unpack("BI", recievedPacket[1+fileNameLength : 5+fileNameLength])
    fileData = struct.unpack("1024s", recievedPacket[5+fileNameLength:])

    if flag == FIRST_PACKAGE:
        with open(fileName, "xb") as f:
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
        if fileChecksum != fileData:
            os.remove(f"./{fileName}")

