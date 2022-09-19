Alunos: Getúlio Coimbra Regis e Igor Lara Oliveira

Como executar:
    python3 exercicio1.py
    python3 exercicio2_client.py
    python3 exercicio2_servidor.py
 
Bibliotecas usadas:
    socket <- criar o socket
    hashlib <- encriptar a senha
    os <- navegar no sistema de arquivo
    logging <- logging
    threading <- criar threads
    struct <- converter para bytes
    exercicio2_utils <- tipos do exercicio 2 e funções para ajudar

Exemplo de uso:
    python3 exercicio1.py <- Iniciar o servidor e com um cliente textual conectar no servidor os comandos são exatamente iguais o do pdf para autenticar é usado CONNECT usuario,senhaemmd5

    python3 exercicio2_servidor.py <- Inicia o servidor
    python3 exercicio2_client.py <- Comandos tem o mesmo nome do pdf os arquivos para serem transferidos devem estar na mesma pasta do cliente para ele conseguir abrir e pegar os bytes, a transferencia demora mas funciona