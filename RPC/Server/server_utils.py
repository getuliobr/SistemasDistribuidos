"""
    Descrição: Utilitarios para o servidor
    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
    Creation Date: 26 / 10 / 2022
"""

# Tipo dos comandos

COMMAND_CREATE = 0x01
COMMAND_READ   = 0x02
COMMAND_LIST   = 0x03
COMMAND_UPDATE = 0x04
COMMAND_DELETE = 0x05
COMMAND_LISTALUNOFROMDISCIPLINA = 0x06
COMMAND_LISTADNFFROMAS = 0x07

# Tipo das classes

CLASS_CURSO = 0X10
CLASS_DISCIPLINA = 0X11
CLASS_ALUNO = 0X12
CLASS_MATRICULA = 0X13
CLASS_MATRICULA_NOTA = 0X14
CLASS_MATRICULA_FALTAS = 0X15
