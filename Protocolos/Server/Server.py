"""
    Descrição: Servidor para listagem e transferência de arquivos com protocolo em binário
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 12 / 09 / 2022
"""

import socket, threading, struct, os, logging
import ProtoFiles.matricula_pb2 as matricula_pb2
from db import *
from Server.server_utils import CLASS_ALUNO, CLASS_CURSO, CLASS_DISCIPLINA

from server_utils import CLASS_MATRICULA, COMMAND_CREATE


# Define o formato de log
log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# Método que cria um cliente
def handleClient(con, client):
    Client(con, client)

# Classe que representa um cliente
class Client:
    def __init__(self, con, client):
        self.con = con
        self.client = client
        self.alive = True
        self.handleEvents() # Inicia a thread
        logging.info("Cliente desconectou")
        self.con.close()
        
    
    def handleEvents(self):
        while self.alive:
            # Recebe o primeiro byte do cabeçalho da mensagem contendo informações sobre o comando
            command = self.con.recv(1)
            command = struct.unpack('B', command)[0]

            if not command:
                break
            
            if command == COMMAND_CREATE:
                print("Recebeu comando de criação")
                type = self.con.recv(1) #Recebe o tipo de objeto a ser criado
                type = struct.unpack('B', type)[0]
                print(type)
                sizeType = self.con.recv(4) #Recebe o tamanho do objeto a ser criado
                sizeType = struct.unpack('I', sizeType)[0]
                print(type, sizeType) 
                data = self.con.recv(sizeType) #Recebe o objeto a ser criado
                if type == CLASS_MATRICULA:
                    matricula = matricula_pb2.Matricula()
                    matricula.ParseFromString(data)
                    try:
                        insert_table("Matricula", (matricula.Ra,
                                            matricula.Cod_disciplina,
                                            matricula.Ano,
                                            matricula.Semestre,
                                            matricula.Nota, 
                                            matricula.Faltas))
                    except Exception as e:
                        logging.error(e)

                if type == CLASS_ALUNO:
                    aluno = matricula_pb2.Aluno()
                    aluno.ParseFromString(data)
                    try:
                        insert_table("Aluno", (aluno.Ra,
                                            aluno.Nome,
                                            aluno.Periodo,
                                            aluno.Cod_curso))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_DISCIPLINA:
                    disciplina = matricula_pb2.Disciplina()
                    disciplina.ParseFromString(data)
                    try:
                        insert_table("Disciplina", (disciplina.Cod_disciplina,
                                            disciplina.Nome,
                                            disciplina.Carga_horaria))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_CURSO:
                    curso = matricula_pb2.Curso()
                    curso.ParseFromString(data)
                    try:
                        insert_table("Curso", (curso.Cod_curso,
                                            curso.Nome))
                    except Exception as e:
                        logging.error(e)
            
            if command == COMMAND_LIST:
                print("Recebeu comando de listagem")
                type = self.con.recv(1) #Recebe o tipo de objeto a ser listado
                type = struct.unpack('B', type)[0]

                if type == CLASS_MATRICULA:
                    matriculas = select_all("Matricula")
                    for matricula in matriculas:
                        matricula = matricula_pb2.Matricula(Ra=matricula[0],
                                                            Cod_disciplina=matricula[1],
                                                            Ano=matricula[2],
                                                            Semestre=matricula[3],
                                                            Nota=matricula[4],
                                                            Faltas=matricula[5])
                        data = matricula.SerializeToString()
                        size = len(data)
                        self.con.send(struct.pack('B', COMMAND_LIST))
                        self.con.send(struct.pack('B', CLASS_MATRICULA))
                        self.con.send(struct.pack('I', size))
                        self.con.send(data)
                
                if type == CLASS_ALUNO:
                    alunos = select_all("Aluno")
                    for aluno in alunos:
                        aluno = matricula_pb2.Aluno(Ra=aluno[0],
                                                    Nome=aluno[1],
                                                    Periodo=aluno[2],
                                                    Cod_curso=aluno[3])
                        data = aluno.SerializeToString()
                        size = len(data)
                        self.con.send(struct.pack('B', COMMAND_LIST))
                        self.con.send(struct.pack('B', CLASS_ALUNO))
                        self.con.send(struct.pack('I', size))
                        self.con.send(data)
                
                if type == CLASS_DISCIPLINA:
                    disciplinas = select_all("Disciplina")
                    for disciplina in disciplinas:
                        disciplina = matricula_pb2.Disciplina(Cod_disciplina=disciplina[0],
                                                            Nome=disciplina[1],
                                                            Carga_horaria=disciplina[2])
                        data = disciplina.SerializeToString()
                        size = len(data)
                        self.con.send(struct.pack('B', COMMAND_LIST))
                        self.con.send(struct.pack('B', CLASS_DISCIPLINA))
                        self.con.send(struct.pack('I', size))
                        self.con.send(data)
                
                if type == CLASS_CURSO:
                    cursos = select_all("Curso")
                    for curso in cursos:
                        curso = matricula_pb2.Curso(Cod_curso=curso[0],
                                                    Nome=curso[1])
                        data = curso.SerializeToString()
                        size = len(data)
                        self.con.send(struct.pack('B', COMMAND_LIST))
                        self.con.send(struct.pack('B', CLASS_CURSO))
                        self.con.send(struct.pack('I', size))
                        self.con.send(data)
            
            if command == COMMAND_UPDATE:
                print("Recebeu comando de atualização")
                type = self.con.recv(1) #Recebe o tipo de objeto a ser atualizado
                type = struct.unpack('B', type)[0]

                sizeType = self.con.recv(4) #Recebe o tamanho do objeto a ser atualizado
                sizeType = struct.unpack('I', sizeType)[0]
                data = self.con.recv(sizeType) #Recebe o objeto a ser atualizado


                # TODO Enviar response de sucesso ou falha
                if type == CLASS_MATRICULA:
                    matricula = matricula_pb2.Matricula()
                    matricula.ParseFromString(data)
                    try:
                        update_table("Matricula", (matricula.nota,
                                                matricula.faltas,
                                                matricula.ra,
                                                matricula.cod_disciplina,
                                                matricula.ano,
                                                matricula.semestre))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_ALUNO:
                    aluno = matricula_pb2.Aluno()
                    aluno.ParseFromString(data)
                    try:
                        update_table("Aluno", (aluno.nome,
                                                aluno.periodo,
                                                aluno.cod_curso,
                                                aluno.ra))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_DISCIPLINA:
                    disciplina = matricula_pb2.Disciplina()
                    disciplina.ParseFromString(data)
                    try:
                        update_table("Disciplina", (disciplina.nome,
                                                disciplina.carga_horaria,
                                                disciplina.cod_disciplina))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_CURSO:
                    curso = matricula_pb2.Curso()
                    curso.ParseFromString(data)
                    try:
                        update_table("Curso", (curso.nome,
                                                curso.cod_curso,
                                                curso.cod_curso))
                    except Exception as e:
                        logging.error(e)
            
            if command == COMMAND_DELETE:
                print("Recebeu comando de deleção")
                type = self.con.recv(1) #Recebe o tipo de objeto a ser deletado
                type = struct.unpack('B', type)[0]

                sizeType = self.con.recv(4) #Recebe o tamanho do objeto a ser deletado
                sizeType = struct.unpack('I', sizeType)[0]
                data = self.con.recv(sizeType) #Recebe o objeto a ser deletado

                if type == CLASS_MATRICULA:
                    matricula = matricula_pb2.Matricula()
                    matricula.ParseFromString(data)
                    try:
                        delete_table("Matricula", (matricula.ra,
                                                matricula.cod_disciplina,
                                                matricula.ano,
                                                matricula.semestre))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_ALUNO:
                    aluno = matricula_pb2.Aluno()
                    aluno.ParseFromString(data)
                    try:
                        delete_table("Aluno", (aluno.ra,))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_DISCIPLINA:
                    disciplina = matricula_pb2.Disciplina()
                    disciplina.ParseFromString(data)
                    try:
                        delete_table("Disciplina", (disciplina.cod_disciplina,))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_CURSO:
                    curso = matricula_pb2.Curso()
                    curso.ParseFromString(data)
                    try:
                        delete_table("Curso", (curso.cod_curso,))
                    except Exception as e:
                        logging.error(e)



                


            

HOST = ''              # Endereco IP do Servidor
PORT = 6666            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket TCP
orig = (HOST, PORT) # Define o endereço do servidor
tcp.bind(orig) # Associa o socket ao endereço
tcp.listen() # Coloca o socket em modo de escuta
while True:
    try:
        logging.info("Servidor aguardando conexão ...")
        con, cliente = tcp.accept() # Espera uma conexão
        logging.info(f"Cliente ({cliente}) conectado --- Criando thread")
        client = threading.Thread(target=handleClient, args=(con, cliente,)) # Cria uma thread para o cliente
        client.start()
    except KeyboardInterrupt:
        print("Servidor encerrado")
        break