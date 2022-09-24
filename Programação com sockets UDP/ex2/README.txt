Alunos: Getúlio Coimbra Regis e Igor Lara Oliveira

->Descrição:
    Programa para envio de arquivos dentro de um cliente para um servidor usando protocolos UDP.

    ->Para a comunicação usamos pacotes com o cabeçalho definido da seguinte forma:

    +---------------------------------------------------------------+
    |        FILE_NAME_SIZE         |           FILE_NAME           |
    +---------------------------------------------------------------+
    |     FLAG      |                 PACKET_NUMBER                 |
    +---------------------------------------------------------------+
    |                           FILEDATA                            |
    +---------------------------------------------------------------+

    -->Tamanhos de cada campo:
        FILE_NAME_SIZE [1 byte]
        FILE_NAME [3-64 byte]
        FLAG [1 byte]
        PACKET_NUMBER [4 bytes]
        FILE_DATA [1024 bytes]
    
    -->Tipos de FLAGS utilizadas:
        0x01 : Primeiro pacote contem o nome do arquivo e tamanho do arquivo
        0X02 : Pacotes que estão no meio e contem só dados do arquivo e qual é o número do pacote, importante porque pode chegar fora de ordem devido a natureza do UDP
        0X03 : Último pacote que contem o checksum
        0x04 : Pacote de confirmação de recebimento de arquivo
        0x05 : Pacote que informa arquivo corrompido


->Como executar:
    -->Servidor:
        python3 ex2_server.py

    -->Cliente:
        python3 gui.py (Interface gráfica)
        ou
        python3 ex2_client.py (Necessita criar variavel de inicialização no arquivo)


->Bibliotecas usadas:
    socket <->> criar o socket
    hashlib <->> checksum
    os <->> navegar no sistema de arquivo
    logging <->> logging
    threading <->> criar threads
    struct <->> converter para bytes
    ex2_utils <->> tipos do exercicio 2 e funções para ajudar
    tkinter <->> interface gráfica

->Exemplo de uso:
    -->Servidor
        python3 ex2_server <->> Inicia servidor

        --->Observações:
            Criar pasta "server_file" no mesmo diretório do servidor

    -->Cliente com interface
        python3 gui.py <->> Inicia interface gráfica

        *Selecionar o arquivo pelo botão de escolha de arquivo
        *Enviar pelo botão de upload
    
    -->Cliente sem interface
        python3 ex2_client.py <->> Inicia cliente

        upload <nome do arquivo> <->> Envia arquivo para o servidor