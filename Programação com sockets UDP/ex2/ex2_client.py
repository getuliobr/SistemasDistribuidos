import socket, os, struct
from ex2_utils import *

ip = "127.0.0.1"
portServer = 6001
portClient = 6000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, portClient))

def sendHeader(fileName, flag, packet_number, data):
    fileName = bytes(fileName, 'ascii')
    packed_request = struct.pack(f"B{len(fileName)}sBI{len(data)}s"
                                , len(fileName)
                                , fileName
                                , flag
                                , packet_number
                                , data
                                )
    s.send(packed_request, (ip, portServer))

def userInput():
    uInput = input().split(" ", 1)
    
    if uInput[0] == "upload":
        if os.path.exists(uInput[1]):
            with open(uInput[1], "rb") as f:
                pass
                
        else:
            print("Arquivo não existe")