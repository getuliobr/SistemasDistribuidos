import sqlite3
from server_utils import *


db = sqlite3.connect('./DB/db.db')
cursor = db.cursor()

def select_all(type):
    cursor.execute("SELECT * FROM " + type)
    return cursor.fetchall()

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