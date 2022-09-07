from http import client
import socket, threading, hashlib


users = {
    'getulio': '12345678',
    'admin': 'admin'
}

def handleClient(con):
    Client(con)

class Client:
    def __init__(self, con):
        self.con = con
        self.alive = True
        self.loggedin = False
        self.loginAttempts = 0
        self.receive()
        print('Cliente desconectou')
        self.con.close()
        
    def receive(self):
        while self.alive:
            msg = (self.con.recv(1024)).decode()
            if msg == 'EXIT' or not msg:
                self.alive = False
                break
            msg = msg.split(' ')
            command = msg[0]
            if command == 'CONNECT' and not self.loggedin:
                self.loginAttempts += 1
                if self.loginAttempts >= 4:
                    self.alive = False
                    break
                
                user, password = msg[1].split(',')
                
                if(hashlib.sha512(users[user].encode("utf-8")).hexdigest() != password):
                    continue
                self.loggedin = True
            
            if not self.loggedin:
                continue

            print(msg)

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
    
    
