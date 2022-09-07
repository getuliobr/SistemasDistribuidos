from http import client
import socket, threading



def handleClient(con):
    Client(con)

class Client:
    def __init__(self, con):
        self.con = con
        self.alive = True
        self.send = threading.Thread(target=self.sendThread)
        self.send.start()
        self.receiveThread()
        print('Cliente desconectou')
        self.con.close()
        
    def receiveThread(self):
        while self.alive:
            msg = (self.con.recv(1024)).decode()
            if msg == 'PARAR' or not msg:
                self.alive = False
                break
            print(msg)

    def sendThread(self):
        while self.alive:
            msg = input()
            if not self.alive:
                break
            self.con.send(msg.encode())
            if msg == 'PARAR':
                self.alive = False
                break

HOST = ''              # Endereco IP do Servidor
PORT = 6666            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
while True:
    print("Servidor aguardando conexao ...");

    con, cliente = tcp.accept()
    print("Cliente conectado ... Criando thread ...");
    client = threading.Thread(target=handleClient, args=(con,))
    client.start()
    
    
