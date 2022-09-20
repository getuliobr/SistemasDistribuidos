"""
    Descrição: Servidor para listagem de arquivos e pastas com autenticação
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 12 / 09 / 2022
"""

import socket, hashlib, os

# Lista de usuarios e senhas
users = {
    'getulio': '12345678',
    'igor': '12345678',
    'admin': 'admin'
}

# Classe do Client
class Client:
    def __init__(self, con):
        self.con = con
        self.alive = True
        self.loggedin = False # Bool de verificação de login
        self.loginAttempts = 0 # Contador de tentativas de login
        self.receive() # Inicia a thread de recebimento
        print('Cliente desconectou')
        self.con.close()
    
    # Função de recebimento
    def receive(self):
        while self.alive:
            # Recebe a mensagem
            msg = (self.con.recv(1024)).decode("utf-8")

            # Se mensagem for EXIT, encerra a conexão
            if msg == 'EXIT' or not msg:
                self.alive = False
                break

            # Trata a mensagem
            msg = msg.split(' ')
            command = msg[0]

            # Se o usuário não estiver logado, verifica se a mensagem é LOGIN
            if command == 'CONNECT' and not self.loggedin:
                self.loginAttempts += 1
                if self.loginAttempts >= 4:
                    self.alive = False
                    break
                
                user, password = msg[1].split(',')

                # Verifica se o usuário existe, e se a senha está correta
                if(hashlib.sha512(users[user].encode("utf-8")).hexdigest() != password):
                    self.con.send(('ERROR').encode("utf-8"))
                    continue
                self.loggedin = True
                self.con.send(('SUCCESS').encode("utf-8"))

            # Se o usuario estiver logado e mensagem PWD, envia o diretório atual
            if command == 'PWD' and self.loggedin:
                self.con.send(os.getcwd().encode("utf-8"))
            
            # Se o usuario estiver logado e mensagem CHDIR, muda o diretório atual com o diretorio passado pelo usuario
            if command == 'CHDIR' and self.loggedin:
                try:
                    os.chdir(msg[1])
                    self.con.send(('SUCCESS').encode("utf-8"))
                except:
                    self.con.send(('ERROR').encode("utf-8"))

            # Se o usuario estiver logado e mensagem GETFILES, envia a lista de arquivos
            if command == 'GETFILES' and self.loggedin:
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                self.con.send(str(len(files)).encode("utf-8"))
                for file in files:
                    self.con.send(str(file + '\n').encode("utf-8"))
            
            # Se o usuario estiver logado e mensagem GETDIRS, envia a lista de pastas
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
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria o socket TCP
orig = (HOST, PORT) # Define o endereço do servidor
tcp.bind(orig) # Vincula o socket ao endereço
tcp.listen(1) # Coloca o socket para escutar
while True:
    print("Servidor aguardando conexao ...")
    con, cliente = tcp.accept() # Aceita a conexão
    pid = os.fork() # Cria um processo filho para atender o cliente
    if pid == 0:
        Client(con)
        break