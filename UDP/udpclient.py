import socket, threading

serverIP     = input('IP: ')
serverPort   = int(input('Porta: '))
bufferSize  = 1024
address = (serverIP, serverPort)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def receiveThread(address):
    while True:
        msg, address = UDPClientSocket.recvfrom(bufferSize)
        message = msg.decode(encoding='utf-8')
        print('RECEIVED:', message)

t = threading.Thread(target=receiveThread, args=(address,))
t.start()

while(True):
    bytesToSend = input('').encode(encoding='utf-8')
    UDPClientSocket.sendto(bytesToSend, address)

    
