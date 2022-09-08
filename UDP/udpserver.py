import socket, threading

localIP     = "127.0.0.1"
localPort   = 6666
bufferSize  = 1024
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
msg, address = bytesAddressPair

def sendThread(address):
    while True:
        bytesToSend = input().encode(encoding='utf-8')
        UDPServerSocket.sendto(bytesToSend, address)

t = threading.Thread(target=sendThread, args=(address,))
t.start()

while(True):
    msg, address = bytesAddressPair
    print('RECEIVED:', msg.decode('utf-8'))
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
