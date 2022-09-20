import socket
import threading
import os
import struct

from ex1_utils import *

ip = "127.0.0.1"
port = input("Digite o numero da porta: ")
name = input("Digite seu nome (Max 64 caracteres): ")
while len(name) > 64 or not len(name):
    name = input("Digite seu nome (Max 64 caracteres): ")  
namesInBytes = bytes(name, 'ascii')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, int(port)))

def help():
    print("------------------ Comandos ------------------")
    print("help - Mostra os comandos disponiveis")
    print("msg - Envia uma mensagem")
    print("emoji - Envia um emoji")
    print("UrL - Envia um link")
    print("ECHO - Verificação se o usuario está online")
    print("quit - Sai do chat")
    print("----------------------------------------------")

def inputThread():

    ip, port = input("Digite o IP e a porta do servidor: ").split()
    help()
    while True:
        userInput = input().split(" ", 1)

        if userInput[0] == "help":
            help()
        
        if userInput[0] == "quit":
            os._exit(1)
        
        if userInput[0] == "msg":
            if len(userInput[1]) > 255:
                print("Mensagem muito grande")
                continue

            msgInBytes = bytes(userInput[1], 'ascii')
            packedRequest = struct.pack(f"BB{len(name)}sB{len(userInput[1])}s",
                                        MESSAGE_TYPE_NORMAL,
                                        len(name),
                                        namesInBytes,
                                        len(userInput[1]),
                                        msgInBytes
                                        )
            s.sendto(packedRequest, (ip, int(port)))
        
        if userInput[0] == "emoji":
            if len(userInput[1]) > 255:
                print("Mensagem muito grande")
                continue

            msgInBytes = bytes(userInput[1], 'utf-8')
            packedRequest = struct.pack(f"BB{len(name)}sB{len(userInput[1])}s",
                                        MESSAGE_TYPE_EMOJI,
                                        len(name),
                                        namesInBytes,
                                        len(userInput[1]),
                                        msgInBytes
                                        )
            s.sendto(packedRequest, (ip, int(port)))
        
        if userInput[0] == "url":
            if len(userInput[1]) > 255:
                print("Mensagem muito grande")
                continue

            msgInBytes = bytes(userInput[1], 'ascii')
            packedRequest = struct.pack(f"BB{len(name)}sB{len(userInput[1])}s",
                                        MESSAGE_TYPE_URL,
                                        len(name),
                                        namesInBytes,
                                        len(userInput[1]),
                                        msgInBytes
                                        )
            s.sendto(packedRequest, (ip, int(port)))
        
        if userInput[0] == "echo":
            print("Sending Ping")
            msgInBytes = bytes("Ping", 'ascii')
            packedRequest = struct.pack(f"BB{len(name)}sB{len('Ping')}s",
                                        MESSAGE_TYPE_ECHO,
                                        len(name),
                                        namesInBytes,
                                        len('Ping'),
                                        msgInBytes
                                        )
            s.sendto(packedRequest, (ip, int(port)))



def receiveThread():
    while True:
        receivedPacket, address = s.recvfrom(323)
        msgType, nameLength, = struct.unpack("BB", receivedPacket[0:2])
        name, = struct.unpack(f"{nameLength}s", receivedPacket[2:2+nameLength])
        msgLength, = struct.unpack("B", receivedPacket[2+nameLength:3+nameLength])
        msg, = struct.unpack(f"{msgLength}s", receivedPacket[3+nameLength:3+nameLength+msgLength])

        if msgType == MESSAGE_TYPE_NORMAL:
            msg = msg.decode('ascii')
            name = name.decode('ascii')
            print(f"{name}>> {msg}")

        if msgType == MESSAGE_TYPE_URL:
            msg = msg.decode('ascii')
            name = name.decode('ascii')
            print(f"{name} enviou o link {msg}")
        
        if msgType == MESSAGE_TYPE_EMOJI:
            msg = msg.decode('utf-8')
            name = name.decode('ascii')
            print(f"{name} enviou o emoji {msg}")
        
        if msgType == MESSAGE_TYPE_ECHO:
            if msg.decode('ascii') == "Ping":
                msg = bytes("Pong", 'ascii')
                packedRequest = struct.pack(f"BB{len(name)}sB{len(msg)}s",
                                            MESSAGE_TYPE_ECHO,
                                            len(name),
                                            namesInBytes,
                                            len(msg),
                                            msg
                                            )
                s.sendto(packedRequest, address)
            else:
                print("Pong!")


            


sendThread = threading.Thread(target=inputThread)
receiveThread = threading.Thread(target=receiveThread)

sendThread.start()
receiveThread.start()
