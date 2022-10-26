Alunos: Getúlio Coimbra Regis e Igor Lara Oliveira

--> Descrição:
    Programa para comunicação TCP entre Cliente e Servidor com linguagens de programação diferentes
    que utilizam RPC para se comunicar, utilizamos o gRPC do google.

--> Dependências
    
    -> Python:
        - pip(pip3)
        - protobuf -> { pip3 install protobuf }
        - grpcio -> { pip3 install grpcio }

    -> Go:
        - protobuf  -> { go install google.golang.org/protobuf/cmd/protoc-gen-go@latest} 
        - grpcio -> { go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest }
    
    -> Caso o arquivo pb de cada linguagem não exista, deverá ser instalado o protobuf e seguir
    o tutorial do site para a criação do mesmo

--> Como executar:
    Cliente:
        cd Client/Classes
        go run Client.go

    Servidor:
        cd Server
        python3 Server.py

--> Bibliotecas usadas
    -> Python:
        - protobuf <-> Para a comunicação externa
        - socket <-> Criar o socket
        - threading <-> Criar threads de clientes
        - logging <-> Fazer os logs
        - struct <-> Para fazer a transformações
        - server_util <-> Tipos de comandos e classes para comunicação
        - sqlite3 <-> Para comunicação com o banco de dados
        - classes_pb2_grpc <-> Arquivo com as definições dos protocolos
        - grpc <-> Para a comunicação externa

    -> Go:
        - encoding/binary <-> Para transformações em bytes
        - fmt <-> Para I/O do programa
        - log <-> Para fazer os logs
        - net <-> Para a conexão socket
        - os <-> Para a manipulação do sistema operacional
        - strings <-> Para tratamento de strings
        - Client/classes <-> Biblioteca com as definições dos protocolos
        - protobuf <-> Para comunicação externa
        - grpc <-> Para comunicação externa

--> Exemplo de uso:
    -> Client:
        -> Criar matricula
            Comandos a serem digitados para criar uma matricula: 
                insertMatricula
                (dados pedidos)

        -> Atualizar notas de matricula 
            Comandos a serem digitados para atualizar notas:
                updateNotas
                (dados pedidos)

        -> Atualizar faltas de matricula
            Comandos a serem digitados para atualizar faltas:
                updateFaltas
                (dados pedidos)

        -> Listagem de alunos (RA, nome, periodo) de acordo com disciplina, ano e semestre
            Comandos a serem digitados para a listagem:
                getAlunos
                (dados pedidos)
        
        -> Listagem de Disciplinas, Faltas e Notas de acordo com ano e semestre
            Comandos a serem digitados para a listagem:
                getDisciplinas
                (dados pedidos)

    -> Servidor
        -> Ele não tem nenhum comando proprio, ele só recebe e responde comandos do cliente