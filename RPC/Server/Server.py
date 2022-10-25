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
        return request
    def UpdateNota(self, request, context):
        print("UpdateNota")
        return classes_pb2.Matricula()
    def UpdateFaltas(self, request, context):
        print("UpdateFaltas")
        return classes_pb2.Matricula()
    def GetAlunos(self, request, context):
        print("GetAlunos")
        return classes_pb2.ListAlunoResponse()

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