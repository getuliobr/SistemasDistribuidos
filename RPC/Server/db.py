import sqlite3
from server_utils import *

# Cria uma conexão com o banco de dados, nesse caso é o arquivo db.db
db = sqlite3.connect('db.db', check_same_thread=False)
# Cria um cursor, ele que faz as chamadas do banco de dados
cursor = db.cursor()

# Seleciona tudo de determinada tabela
def select_all(type):
    cursor.execute(f"SELECT * FROM {type.upper()}")
    return cursor.fetchall()

# Seleciona dados de determinada tabela dependendo dos parametros
def select_table(type, data):
    if type == CLASS_MATRICULA:
        cursor.execute("SELECT * FROM Matricula WHERE ra = ? AND cod_disciplina = ? AND ano = ? AND semestre = ?", data)
        return cursor.fetchall()
    if type == CLASS_ALUNO:
        cursor.execute(f"SELECT * FROM Aluno WHERE ra = '{data}'")
        return cursor.fetchall()
    if type == CLASS_CURSO:
        cursor.execute("SELECT * FROM Curso WHERE codigo = ?", data)
        return cursor.fetchall()
    if type == CLASS_DISCIPLINA:
        cursor.execute(f"SELECT * FROM Disciplina WHERE codigo = '{data}'")
        return cursor.fetchall()
# Insere dados em determinada tabela
def insert_table(type, data):
    if type == CLASS_MATRICULA:
        cursor.execute("INSERT INTO Matricula (ra, cod_disciplina, ano, semestre, nota, faltas) VALUES (?, ?, ?, ?, ?, ?)", data)
        db.commit()
    if type == CLASS_ALUNO:
        cursor.execute("INSERT INTO Aluno (ra, nome, periodo, cod_curso) VALUES (?, ?, ?, ?)", data)
        db.commit()
    if type == CLASS_CURSO:
        cursor.execute("INSERT INTO Curso (codigo, nome) VALUES (?, ?)", data)
        db.commit()
    if type == CLASS_DISCIPLINA:
        cursor.execute("INSERT INTO Disciplina (codigo, nome, professor, cod_curso) VALUES (?, ?, ?, ?)", data)
        db.commit()
# Atualiza dados em determinada tabela
def update_table(type, data):
    if type == CLASS_MATRICULA:
        cursor.execute("UPDATE Matricula SET nota = ?, faltas = ? WHERE ra = ? AND cod_disciplina = ? AND ano = ? AND semestre = ?", data)
        db.commit()
    if type == CLASS_ALUNO:
        cursor.execute("UPDATE Aluno SET nome = ?, periodo = ?, cod_curso = ? WHERE ra = ?", data)
        db.commit()
    if type == CLASS_CURSO:
        cursor.execute("UPDATE Curso SET nome = ?, SET codigo = ? WHERE codigo = ?", data)
        db.commit()
    if type == CLASS_DISCIPLINA:
        cursor.execute("UPDATE Disciplina SET nome = ?, professor = ?, cod_curso = ? WHERE codigo = ?", data)
        db.commit()
# Exclui dados em determinada tabela
def delete_table(type, data):
    if type == CLASS_MATRICULA:
        cursor.execute("DELETE FROM Matricula WHERE ra = ? AND cod_disciplina = ? AND ano = ? AND semestre = ?", data)
        db.commit()
    if type == CLASS_ALUNO:
        cursor.execute("DELETE FROM Aluno WHERE ra = ?", data)
        db.commit()
    if type == CLASS_CURSO:
        cursor.execute("DELETE FROM Curso WHERE codigo = ?", data)
        db.commit()
    if type == CLASS_DISCIPLINA:
        cursor.execute("DELETE FROM Disciplina WHERE codigo = ?", data)
        db.commit()