"""
    Descrição: Ferramentas e dados uteis para o servidor e cliente de transferência de arquivos com protocolo binário
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 12 / 09 / 2022
"""

# São os valoras passados no enunciado da questão
MESSAGE_TYPE_REQUEST = 0x01
MESSAGE_TYPE_RESPONSE = 0x02

STATUS_SUCCESS = 0x01
STATUS_ERROR = 0x02

COMMAND_ADDFILE = 0x01
COMMAND_DELETE = 0x02
COMMAND_GETFILESLIST = 0x03
COMMAND_GETFILE = 0x04

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