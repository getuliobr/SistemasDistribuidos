import logging
import grpc
import time
from concurrent import futures
from db import *
import classes_pb2
import classes_pb2_grpc

log = logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

class TesteService(classes_pb2_grpc.TesteServiceServicer):
    def AddMatricula(self, request, context):
        try:
            insert_table(CLASS_MATRICULA, ( request.RA,
                                            request.Cod_disciplina,
                                            request.Ano,
                                            request.Semestre,
                                            request.Nota, 
                                            request.Faltas))
            logging.info("Matricula inserida com sucesso")
        except Exception as e:
            logging.error("Erro ao inserir matricula:", e)
            return classes_pb2.Matricula(RA=0)
        return classes_pb2.Matricula(RA=1)

    def UpdateNota(self, request, context):
        try:
            update_table(CLASS_MATRICULA_NOTA, (request.Nota, request.RA, request.Cod_disciplina, request.Ano, request.Semestre))
            a = select_table(CLASS_MATRICULA, (request.RA, request.Cod_disciplina, request.Ano, request.Semestre))[0]
            
            logging.info("Nota atualizada com sucesso")
        except Exception as e:
            logging.error("Erro ao atualizar nota:", e)
            return classes_pb2.Matricula(RA=0)
        return classes_pb2.Matricula(RA=1)

    def UpdateFaltas(self, request, context):
        try:
            update_table(CLASS_MATRICULA_FALTAS, (request.Faltas, request.RA, request.Cod_disciplina, request.Ano, request.Semestre))
            logging.info("Faltas atualizadas com sucesso")
        except Exception as e:
            logging.error("Erro ao atualizar faltas:", e)
            return classes_pb2.Matricula(RA=0)
        return classes_pb2.Matricula(RA=1)

    def GetAlunos(self, request, context):
        try:
            cursor.execute(f"SELECT ra, nome, periodo, cod_curso from Aluno WHERE RA IN (SELECT RA FROM MATRICULA WHERE cod_disciplina = ? AND ano = ? AND semestre = ?)", (request.Cod_disciplina, request.Ano, request.Semestre))
            alunos = cursor.fetchall()
            response = classes_pb2.AlunoResponse()
            for aluno in alunos:
                response.Alunos.append(classes_pb2.Aluno(RA=aluno[0], Nome=aluno[1], Periodo=aluno[2], Cod_curso=aluno[3]))

            logging.info("Alunos selecionados com sucesso")
            return response
        except Exception as e:
            logging.error("Erro ao selecionar alunos:", e)
            return classes_pb2.AlunoResponse()
    
    def GetDisciplinas(self, request, context):
        try:
            cursor.execute("SELECT d.codigo, d.nome, m.ra, a.nome, m.nota, m.faltas from Matricula m INNER JOIN Aluno a INNER JOIN Disciplina d WHERE m.ra = a.ra AND d.codigo = m.cod_disciplina AND m.ano = ? AND m.semestre = ? ", (request.Ano, request.Semestre))
            values = cursor.fetchall()
            response = classes_pb2.DisciplinaResponse()
            for value in values:
                response.Disciplinas.append(classes_pb2.DisciplinaNomesNotasEFaltas(Cod_disciplina=value[0], Nome=value[1], Nota=value[4], Faltas=value[5]))
            logging.info("Disciplinas selecionadas com sucesso")
            return response
        except Exception as e:
            logging.error("Erro ao selecionar disciplinas:", e)
            return classes_pb2.DisciplinaResponse()

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# to add the defined class to the server
classes_pb2_grpc.add_TesteServiceServicer_to_server(TesteService(), server)

print('Starting server. Listening on port 6677.')
server.add_insecure_port('[::]:6677')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)