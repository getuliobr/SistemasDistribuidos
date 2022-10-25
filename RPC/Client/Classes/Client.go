package main

import (
	"context"
	"fmt"
	"log"

	classes "Client/classes"

	grpc "google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	var conn *grpc.ClientConn
	conn, err := grpc.Dial(":6677", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %s", err)
	}
	defer conn.Close()

	usr := classes.NewTesteServiceClient(conn)

	for {
		var input string
		fmt.Println("Digite o comando:")
		fmt.Scanln(&input)

		if input == "insertMatricula" {
			var ra int32
			var codDisciplina string
			var ano int32
			var semestre int32
			var nota float32 = 0
			var faltas int32 = 0
			fmt.Println("Digite o RA:")
			fmt.Scanln(&ra)
			fmt.Println("Digite o codDisciplina:")
			fmt.Scanln(&codDisciplina)
			fmt.Println("Digite o ano:")
			fmt.Scanln(&ano)
			fmt.Println("Digite o semestre:")
			fmt.Scanln(&semestre)
			fmt.Println("Digite a nota:")
			fmt.Scanln(&nota)
			fmt.Println("Digite o faltas:")
			fmt.Scanln(&faltas)
			newMatricula := &classes.Matricula{
				RA:            ra,
				CodDisciplina: codDisciplina,
				Ano:           ano,
				Semestre:      semestre,
				Nota:          nota,
				Faltas:        faltas,
			}

			response, err := usr.AddMatricula(context.Background(), newMatricula)
			if err != nil {
				log.Fatalf("Erro no CreateMatricula: %s", err)
			}
			log.Printf("Matricula criada:")
			log.Println(response)
		}

		if input == "updateNota" {
			var ra int32
			var codDisciplina string
			var ano int32
			var semestre int32
			var nota float32 = 0
			fmt.Println("Digite o RA:")
			fmt.Scanln(&ra)
			fmt.Println("Digite o codDisciplina:")
			fmt.Scanln(&codDisciplina)
			fmt.Println("Digite o ano:")
			fmt.Scanln(&ano)
			fmt.Println("Digite o semestre:")
			fmt.Scanln(&semestre)
			fmt.Println("Digite a nota:")
			fmt.Scanln(&nota)
			newRequestNota := &classes.UpdateNotaRequest{
				RA:            ra,
				CodDisciplina: codDisciplina,
				Ano:           ano,
				Semestre:      semestre,
				Nota:          nota,
			}
			response, err := usr.UpdateNota(context.Background(), newRequestNota)
			if err != nil {
				log.Fatalf("Erro no UpdateNota: %s", err)
			}
			log.Printf("Nota atualizada:")
			log.Println(response)
		}

		if input == "updateFaltas" {
			var ra int32
			var codDisciplina string
			var ano int32
			var semestre int32
			var faltas int32 = 0
			fmt.Println("Digite o RA:")
			fmt.Scanln(&ra)
			fmt.Println("Digite o codDisciplina:")
			fmt.Scanln(&codDisciplina)
			fmt.Println("Digite o ano:")
			fmt.Scanln(&ano)
			fmt.Println("Digite o semestre:")
			fmt.Scanln(&semestre)
			fmt.Println("Digite o faltas:")
			fmt.Scanln(&faltas)
			newRequestFaltas := &classes.UpdateFaltasRequest{
				RA:            ra,
				CodDisciplina: codDisciplina,
				Ano:           ano,
				Semestre:      semestre,
				Faltas:        faltas,
			}
			response, err := usr.UpdateFaltas(context.Background(), newRequestFaltas)
			if err != nil {
				log.Fatalf("Erro no UpdateFaltas: %s", err)
			}
			log.Printf("Faltas atualizadas:")
			log.Println(response)
		}

		if input == "getAlunos" {
			var codDisciplina string
			var ano int32
			var semestre int32
			fmt.Println("Digite o codDisciplina:")
			fmt.Scanln(&codDisciplina)
			fmt.Println("Digite o ano:")
			fmt.Scanln(&ano)
			fmt.Println("Digite o semestre:")
			fmt.Scanln(&semestre)
			newRequestAlunos := &classes.AlunoRequest{
				CodDisciplina: codDisciplina,
				Ano:           ano,
				Semestre:      semestre,
			}

			response, err := usr.GetAlunos(context.Background(), newRequestAlunos)
			if err != nil {
				log.Fatalf("Erro no GetAlunos: %s", err)
			}
			if len(response.Alunos) == 0 {
				log.Printf("Nenhum aluno encontrado")
			} else {
				log.Printf("Lista de Alunos:")
				for _, aluno := range response.Alunos {
					log.Println(aluno)
				}
			}
		}

		if input == "getDisciplinas" {
			var ano int32
			var semestre int32
			fmt.Println("Digite o ano:")
			fmt.Scanln(&ano)
			fmt.Println("Digite o semestre:")
			fmt.Scanln(&semestre)
			newRequestDisciplinas := &classes.DisciplinaRequest{
				Ano:      ano,
				Semestre: semestre,
			}

			response, err := usr.GetDisciplinas(context.Background(), newRequestDisciplinas)
			if err != nil {
				log.Fatalf("Erro no GetDisciplinas: %s", err)
			}
			if len(response.Disciplinas) == 0 {
				log.Printf("Nenhuma disciplina encontrada")
			} else {
				log.Printf("Lista de Disciplinas:")
				for _, disciplina := range response.Disciplinas {
					log.Println(disciplina)
				}
			}
		}

		if input == "sair" {
			break
		}
	}
}
