"""
    Descrição: Ferramentas e dados uteis para as conexões do cliente e servidor com protocolo binário
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 19 / 09 / 2022
"""
FIRST_PACKAGE = 0x01
PACKAGE_DATA = 0x02
LAST_PACKAGE = 0x03
UPLOAD_SUCCESSFULL = 0x04
UPLOAD_FAILED = 0x05

FILE_DATA_SIZE = 1024