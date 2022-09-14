"""
    Descrição: Servidor para listagem de arquivos e pastas com autenticação
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 12 / 09 / 2022
"""

import socket, threading, hashlib, os


users = {
    'getulio': '12345678',
    'igor': '12345678',
    'admin': 'admin'
}

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
            msg = (self.con.recv(1024)).decode("utf-8")
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
                    self.con.send(('ERROR').encode("utf-8"))
                    continue
                self.loggedin = True
                self.con.send(('SUCCESS').encode("utf-8"))

            
            if command == 'PWD' and self.loggedin:
                self.con.send(os.getcwd().encode("utf-8"))
            
            if command == 'CHDIR' and self.loggedin:
                try:
                    os.chdir(msg[1])
                    self.con.send(('SUCCESS').encode("utf-8"))
                except:
                    self.con.send(('ERROR').encode("utf-8"))

            if command == 'GETFILES' and self.loggedin:
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                self.con.send(str(len(files)).encode("utf-8"))
                for file in files:
                    self.con.send(str(file + '\n').encode("utf-8"))
            
            if command == 'GETDIRS' and self.loggedin:
                files = [f for f in os.listdir('.') if not os.path.isfile(f)]
                self.con.send(str(len(files)).encode("utf-8"))
                for file in files:
                    self.con.send(str(file + '\n').encode("utf-8"))
            

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
    print("Servidor aguardando conexao ...")
    con, cliente = tcp.accept()
    pid = os.fork()
    if pid == 0:
        Client(con)
        break