"""
    Descrição: Servidor para listagem e transferência de arquivos com protocolo em binário
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 12 / 09 / 2022
"""

import socket, threading, struct, os, logging
from classes_pb2 import Aluno, Curso, Disciplina, Matricula
from db import *
from server_utils import *


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
                sizeType = self.con.recv(4) #Recebe o tamanho do objeto a ser criado
                sizeType = struct.unpack('I', sizeType)[0]
                data = self.con.recv(sizeType) #Recebe o objeto a ser criado
                if type == CLASS_MATRICULA:
                    matricula = Matricula()
                    matricula.ParseFromString(data)
                    try:
                        insert_table(CLASS_MATRICULA, (matricula.RA,
                                            matricula.Cod_disciplina,
                                            matricula.Ano,
                                            matricula.Semestre,
                                            matricula.Nota, 
                                            matricula.Faltas))
                        logging.info("Matricula criada com sucesso")
                    except Exception as e:
                        logging.error(e)

                if type == CLASS_ALUNO:
                    aluno = Aluno()
                    aluno.ParseFromString(data)
                    try:
                        insert_table(CLASS_ALUNO, (aluno.Ra,
                                            aluno.Nome,
                                            aluno.Periodo,
                                            aluno.Cod_curso))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_DISCIPLINA:
                    disciplina = Disciplina()
                    disciplina.ParseFromString(data)
                    try:
                        insert_table(CLASS_DISCIPLINA, (disciplina.Cod_disciplina,
                                            disciplina.Nome,
                                            disciplina.Carga_horaria))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_CURSO:
                    curso = Curso()
                    curso.ParseFromString(data)
                    try:
                        insert_table(CLASS_CURSO, (curso.Cod_curso,
                                            curso.Nome))
                    except Exception as e:
                        logging.error(e)
            
            if command == COMMAND_LIST:
                print("Recebeu comando de listagem")
                type = self.con.recv(1) #Recebe o tipo de objeto a ser listado
                type = struct.unpack('B', type)[0]

                if type == CLASS_MATRICULA:
                    matriculas = select_all("Matricula")
                    size = len(matriculas)
                    self.con.send(struct.pack('I', size))
                    for matricula in matriculas:
                        matricula = Matricula(RA=matricula[0],
                                    Cod_disciplina=matricula[1],
                                    Ano=matricula[2],
                                    Semestre=matricula[3],
                                    Nota=matricula[4],
                                    Faltas=matricula[5])
                        data = matricula.SerializeToString()
                        size = len(data)
                        self.con.send(struct.pack('I', size))    
                        self.con.send(data)
                
                if type == CLASS_DISCIPLINA:
                    disciplinas = select_all("Disciplina")
                    for disciplina in disciplinas:
                        disciplina = Disciplina(Cod_disciplina=disciplina[0],
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
                    matricula = Matricula()
                    matricula.ParseFromString(data)
                    try:
                        update_table(CLASS_MATRICULA, (matricula.nota,
                                                matricula.faltas,
                                                matricula.ra,
                                                matricula.cod_disciplina,
                                                matricula.ano,
                                                matricula.semestre))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_ALUNO:
                    aluno = Aluno()
                    aluno.ParseFromString(data)
                    try:
                        update_table(CLASS_ALUNO, (aluno.nome,
                                                aluno.periodo,
                                                aluno.cod_curso,
                                                aluno.ra))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_DISCIPLINA:
                    disciplina = Disciplina()
                    disciplina.ParseFromString(data)
                    try:
                        update_table(CLASS_DISCIPLINA, (disciplina.Nome,
                                                disciplina.Carga_horaria,
                                                disciplina.Cod_disciplina))
                    except Exception as e:
                        logging.error(e)
                
                if type == CLASS_CURSO:
                    curso = Curso()
                    curso.ParseFromString(data)
                    try:
                        update_table(CLASS_CURSO, (curso.nome,
                                                curso.cod_curso,
                                                curso.cod_curso))
                    except Exception as e:
                        logging.error(e)
            
            if command == COMMAND_LISTALUNOFROMDISCIPLINA:
                print("Recebeu comando de listagem de alunos de uma disciplina")
                sizeDisciplina = self.con.recv(4) #Recebe o tamanho do nome da disciplina
                sizeDisciplina = struct.unpack('I', sizeDisciplina)[0]
                disciplina = self.con.recv(sizeDisciplina) #Recebe o nome da disciplina
                disciplina = disciplina.decode('utf-8')
                ano = self.con.recv(4) #Recebe o ano da matricula
                ano = struct.unpack('I', ano)[0]
                semestre = self.con.recv(4) #Recebe o semestre da matricula
                semestre = struct.unpack('I', semestre)[0]

                cursor.execute(f"SELECT ra, nome, periodo, cod_curso from Aluno WHERE RA IN (SELECT RA FROM MATRICULA WHERE cod_disciplina = ? AND ano = ? AND semestre = ?)", (disciplina, ano, semestre))
                alunos = cursor.fetchall()
                self.con.send(struct.pack('I', len(alunos)))
                for aluno in alunos:
                    aluno = Aluno(RA=aluno[0],
                            Nome=aluno[1],
                            Periodo=aluno[2],
                            Cod_curso=aluno[3])
                    data = aluno.SerializeToString()
                    size = len(data)
                    self.con.send(struct.pack('I', size))
                    self.con.send(data)
            

            #TODO
            if command == COMMAND_LISTADNFFROMAS:
                ano = self.con.recv(4) #Recebe o ano da matricula
                ano = struct.unpack('I', ano)[0]
                semestre = self.con.recv(4) #Recebe o semestre da matricula
                semestre = struct.unpack('I', semestre)[0]

                cursor.execute("SELECT d.nome, m.ra, a.nome, m.nota, m.faltas from Matricula m INNER JOIN Aluno a INNER JOIN Disciplina d WHERE m.ra = a.ra AND d.codigo = m.cod_disciplina AND m.ano = ? AND m.semestre = ? ", (ano, semestre))
                values = cursor.fetchall()
                
                for value in values:
                    disciplina = select_table(CLASS_DISCIPLINA, value[0])
                    matricula = select_table(CLASS_MATRICULA, (value[1], disciplina[0], ano, semestre))
                    aluno = select_table(CLASS_ALUNO, value[1])
                    print(disciplina)
                    print(matricula)
                    print(aluno)


            # if command == COMMAND_DELETE:
            #     print("Recebeu comando de deleção")
            #     type = self.con.recv(1) #Recebe o tipo de objeto a ser deletado
            #     type = struct.unpack('B', type)[0]

            #     sizeType = self.con.recv(4) #Recebe o tamanho do objeto a ser deletado
            #     sizeType = struct.unpack('I', sizeType)[0]
            #     data = self.con.recv(sizeType) #Recebe o objeto a ser deletado

            #     if type == CLASS_MATRICULA:
            #         matricula = matricula_pb2.Matricula()
            #         matricula.ParseFromString(data)
            #         try:
            #             delete_table("Matricula", (matricula.ra,
            #                                     matricula.cod_disciplina,
            #                                     matricula.ano,
            #                                     matricula.semestre))
            #         except Exception as e:
            #             logging.error(e)
                
            #     if type == CLASS_ALUNO:
            #         aluno = matricula_pb2.Aluno()
            #         aluno.ParseFromString(data)
            #         try:
            #             delete_table("Aluno", (aluno.ra,))
            #         except Exception as e:
            #             logging.error(e)
                
            #     if type == CLASS_DISCIPLINA:
            #         disciplina = matricula_pb2.Disciplina()
            #         disciplina.ParseFromString(data)
            #         try:
            #             delete_table("Disciplina", (disciplina.cod_disciplina,))
            #         except Exception as e:
            #             logging.error(e)
                
            #     if type == CLASS_CURSO:
            #         curso = matricula_pb2.Curso()
            #         curso.ParseFromString(data)
            #         try:
            #             delete_table("Curso", (curso.cod_curso,))
            #         except Exception as e:
            #             logging.error(e)



                


            

HOST = ''              # Endereco IP do Servidor
PORT = 6667            # Porta que o Servidor esta
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