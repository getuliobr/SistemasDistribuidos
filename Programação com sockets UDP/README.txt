

FLAG [1 byte]
PACKET_NUMBER [4 bytes]
FILE_DATA [1019 bytes]

Tipos de FLAG:
0x01 : Primeiro pacote contem o nome do arquivo e tamanho do arquivo
0X02 : Pacotes que estão no meio e contem só dados do arquivo e qual é o número do pacote, importante porque pode chegar fora de ordem devido a natureza do UDP
0X03 : Último pacote que contem o checksum 


+---------------------------------------------------------------+
|     FLAG      |                 PACKET_NUMBER                 |
+---------------------------------------------------------------+
|                           FILE_DATA                           |
+---------------------------------------------------------------+