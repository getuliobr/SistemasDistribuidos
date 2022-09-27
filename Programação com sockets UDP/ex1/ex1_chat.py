"""
    Descrição: Arquivo para abertura de um chat com um IP e porta especificos
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 19 / 09 / 2022
"""
import socket
import threading
import os
import struct

from ex1_utils import *

ip = "127.0.0.1" # Endereço local para abrir o servidor do chat
port = input("Digite o numero da porta: ") # Porta que a outra pessoa vai usar para se conectar
name = input("Digite seu nome (Max 64 caracteres): ") # Nome do usuario
while len(name) > 64 or not len(name): # Garantir que o nome serve
    name = input("Digite seu nome (Max 64 caracteres): ")  
namesInBytes = bytes(name, 'ascii') # Codifica o nome do usuario em bytes
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria o socket UDP
s.bind((ip, int(port))) # Cria o servidor UDP propriamente dito

# Função para imprimir os comandos
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

    ip, port = input("Digite o IP e a porta do servidor: ").split() # Pegar o IP e a porta do outro usuario
    help() # Mostrar os comandos
    while True:
        userInput = input().split(" ", 1) # Pegar o comando e a mensagem
        # O comando fica na posição 0 e a mensagem na posição 1
        # Comando help
        if userInput[0] == "help": 
            help()
        
        # Comando quit
        if userInput[0] == "quit":
            os._exit(1)
        
        # Comando msg
        if userInput[0] == "msg":
            if len(userInput[1]) > 255: # Trata o caso de a mensagem ser maior que 255 bytes
                print("Mensagem muito grande")
                continue

            msgInBytes = bytes(userInput[1], 'ascii') # Codifica a mensagem em bytes
            packedRequest = struct.pack(f"BB{len(name)}sB{len(userInput[1])}s",
                                        MESSAGE_TYPE_NORMAL,
                                        len(name),
                                        namesInBytes,
                                        len(userInput[1]),
                                        msgInBytes
                                        ) # Empacota a mensagem, primeiro byte é o tipo, o segundo é o tamanho do nome, depois vem o nome, depois o tamanho da mensagem e por fim a mensagem
            s.sendto(packedRequest, (ip, int(port))) # Envia a mensagem

        # Comando emoji
        if userInput[0] == "emoji":
            if len(userInput[1]) > 255: # Trata o caso de a mensagem ser maior que 255 bytes
                print("Mensagem muito grande")
                continue

            msgInBytes = bytes(userInput[1], 'utf-8') # Codifica a mensagem em bytes importante ser em utf-8 por causa dos emojis
            packedRequest = struct.pack(f"BB{len(name)}sB{len(userInput[1])}s",
                                        MESSAGE_TYPE_EMOJI,
                                        len(name),
                                        namesInBytes,
                                        len(userInput[1]),
                                        msgInBytes
                                        ) # O empacotamento funciona do mesmo jeito do passado so trocando o tipo e o texto da mensagem sendo o emoji
            s.sendto(packedRequest, (ip, int(port))) # Envia a mensagem
        
        # Comando url
        if userInput[0] == "url":
            if len(userInput[1]) > 255: # Trata o caso de a mensagem ser maior que 255 bytes
                print("Mensagem muito grande")
                continue

            msgInBytes = bytes(userInput[1], 'ascii')
            packedRequest = struct.pack(f"BB{len(name)}sB{len(userInput[1])}s",
                                        MESSAGE_TYPE_URL,
                                        len(name),
                                        namesInBytes,
                                        len(userInput[1]),
                                        msgInBytes
                                        ) # O empacotamento funciona do mesmo jeito do passado so trocando o tipo e o texto da mensagem sendo o url
            s.sendto(packedRequest, (ip, int(port))) # Envia a mensagem
        
        # Comando echo
        if userInput[0] == "echo":
            print("Sending Ping")
            msgInBytes = bytes("Ping", 'ascii')
            packedRequest = struct.pack(f"BB{len(name)}sB{len('Ping')}s",
                                        MESSAGE_TYPE_ECHO,
                                        len(name),
                                        namesInBytes,
                                        len('Ping'),
                                        msgInBytes
                                        ) # O empacotamento funciona do mesmo jeito do passado so trocando o tipo e o texto da mensagem é o ping
            s.sendto(packedRequest, (ip, int(port))) # Envia a mensagem


# Função que recebe as mensagens da outra pessoa
def receiveThread():
    while True:
        # Recebe 323 bytes
        receivedPacket, address = s.recvfrom(323)
        # Os dois primeiros bytes são o tipo da mensagem e o tamanho do nome
        msgType, nameLength, = struct.unpack("BB", receivedPacket[0:2])
        # Os próximos bytes até o tamanho do nome são o nome
        name, = struct.unpack(f"{nameLength}s", receivedPacket[2:2+nameLength])
        # O próximo bytes é o tamanho da mensagem
        msgLength, = struct.unpack("B", receivedPacket[2+nameLength:3+nameLength])
        # Os próximos bytes até o tamanho da mensagem são a mensagem
        msg, = struct.unpack(f"{msgLength}s", receivedPacket[3+nameLength:3+nameLength+msgLength])

        # Se a mensagem for do tipo normal só decodifica como ascii
        if msgType == MESSAGE_TYPE_NORMAL:
            msg = msg.decode('ascii')
            name = name.decode('ascii')
            print(f"{name}>> {msg}")

        # Se a mensagem for do tipo url decodifica como ascii e da um print diferente
        if msgType == MESSAGE_TYPE_URL:
            msg = msg.decode('ascii')
            name = name.decode('ascii')
            print(f"{name} enviou o link {msg}")
        
        # Se a mensagem for do tipo emoji decodifica como utf-8
        if msgType == MESSAGE_TYPE_EMOJI:
            msg = msg.decode('utf-8')
            name = name.decode('ascii')
            print(f"{name} enviou o emoji {msg}")
        
        # Se a mensagem for do tipo echo manda uma mensagem de pong de volta e imprime que recebeu um ping
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
