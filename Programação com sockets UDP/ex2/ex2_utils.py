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

# Função que recebe um numero de bytes e retorna uma string formatada com o tamanho
def convertBytesNumber(number):
    if number < 1024:
        return str(number) + " B"
    elif number < 1048576:
        return format(number/1024, '.3f') + " KiB"
    elif number < 1073741824:
        return format(number/1048576, '.3f') + " MiB"
    else:
        return format(number/1073741824, '.3f') + " GiB"