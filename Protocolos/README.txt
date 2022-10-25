Alunos: Getúlio Coimbra Regis e Igor Lara Oliveira

--> Descrição:
    Programa para comunicação TCP entre Cliente e Servidor com linguagens de programação diferentes
    que utilizam de uma forma de representação externa de dados para se comunicar, utilizamos o
    protobuf do google.

    -> Tipos de comandos utilizados para a comunicação:
    0x01 -> Create
    0x02 -> Read
    0x03 -> List
    0x04 -> Update
    0x05 -> Delete
    0x06 -> ListALunosFromDiscplina

    -> Tipos de classe utilizados para a comunicação:
    0x10 -> Curso
    0x11 -> Disciplina
    0x12 -> Aluno
    0x13 -> Matricula

--> Dependências
    
    -> Python:
        - pip(pip3)
        - protobuf -> { pip3 install protobuf }

    -> Go:
        - protobuf  -> { go install google.golang.org/protobuf/cmd/protoc-gen-go@latest} 
    
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
        - classes_pb2 <-> Arquivo com as definições dos protocolos

    -> Go:
        - encoding/binary <-> Para transformações em bytes
        - fmt <-> Para I/O do programa
        - log <-> Para fazer os logs
        - net <-> Para a conexão socket
        - os <-> Para a manipulação do sistema operacional
        - strings <-> Para tratamento de strings
        - Client/classes <-> Biblioteca com as definições dos protocolos
        - protobuf <-> Para comunicação externa

--> Exemplo de uso:
    -> Client:
        -> Criar matricula
            Comandos a serem digitados para criar uma matricula: 
                create
                matricula
                (dados pedidos)

        -> Atualizar matricula (faltas e notas)
            Comandos a serem digitados para atualizar matricula:
                update
                matricula
                (dados pedidos)

        -> Listagem de alunos (RA, nome, periodo) de acordo com disciplina, ano e semestre
            Comandos a serem digitados para a listagem:
                list
                aluno
                (dados pedidos)
        
        -> Listagem de Disciplinas, Faltas e Notas de acordo com ano e semestre
            Comandos a serem digitados para a listagem:
                list 
                disciplinas_ano
                (dados pedidos)

    -> Servidor
        -> Ele não tem nenhum comando proprio, ele só recebe e responde comandos do cliente