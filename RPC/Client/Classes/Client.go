/*
		Descrição: Arquivo para abertura de cliente TCP para comunicação e transferência de dados por protocolo e gRPC (Protobuf)
	  Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
		Creation Date: 26 / 10 / 2022
*/

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
	// Criação de conexão com o servidor
	var conn *grpc.ClientConn
	conn, err := grpc.Dial(":6677", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %s", err)
	}
	defer conn.Close()

	// Cria service de cliente
	usr := classes.NewTesteServiceClient(conn)

	for {
		// Recebe input do usuário para comando
		var input string
		fmt.Println("Digite o comando:")
		fmt.Scanln(&input)

		// Se o comando for insertMatricula, solicita os dados para inserção e insere
		if input == "insertMatricula" {
			// Recebe input do usuário para dados
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
			// Cria objeto matricula para inserção
			newMatricula := &classes.Matricula{
				RA:            ra,
				CodDisciplina: codDisciplina,
				Ano:           ano,
				Semestre:      semestre,
				Nota:          nota,
				Faltas:        faltas,
			}

			// Envia objeto matricula para inserção no servidor
			response, err := usr.AddMatricula(context.Background(), newMatricula)
			if err != nil {
				log.Fatalf("Erro no CreateMatricula: %s", err)
			}
			if response.RA == 1 {
				fmt.Println("Matricula criada com sucesso!")
			} else {
				fmt.Println("Erro ao criar matricula!")
			}
		}

		// Se o comando for updateNota, solicita os dados para atualização e atualiza
		if input == "updateNota" {
			// Recebe input do usuário para dados
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
			// Cria novo objeto de Request para update na nota
			newRequestNota := &classes.UpdateNotaRequest{
				RA:            ra,
				CodDisciplina: codDisciplina,
				Ano:           ano,
				Semestre:      semestre,
				Nota:          nota,
			}
			// Envia objeto para atualização no servidor
			response, err := usr.UpdateNota(context.Background(), newRequestNota)
			if err != nil {
				log.Fatalf("Erro no UpdateNota: %s", err)
			}
			if response.RA == 1 {
				fmt.Println("Nota atualizada com sucesso!")
			} else {
				fmt.Println("Erro ao atualizar nota!")
			}
		}

		// Se o comando for updateFaltas, solicita os dados para atualização e atualiza
		if input == "updateFaltas" {
			// Recebe input do usuário para dados
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
			// Cria novo objeto de Request para update nas faltas
			newRequestFaltas := &classes.UpdateFaltasRequest{
				RA:            ra,
				CodDisciplina: codDisciplina,
				Ano:           ano,
				Semestre:      semestre,
				Faltas:        faltas,
			}
			// Envia objeto para atualização no servidor
			response, err := usr.UpdateFaltas(context.Background(), newRequestFaltas)
			if err != nil {
				log.Fatalf("Erro no UpdateFaltas: %s", err)
			}
			if response.RA == 1 {
				fmt.Println("Faltas atualizadas com sucesso!")
			} else {
				fmt.Println("Erro ao atualizar faltas!")
			}
		}

		// Se o comando for getAlunos, envia requisição para receber lista de alunos, passando codDisciplina, ano e semestre
		if input == "getAlunos" {
			// Recebe input do usuário para dados
			var codDisciplina string
			var ano int32
			var semestre int32
			fmt.Println("Digite o codDisciplina:")
			fmt.Scanln(&codDisciplina)
			fmt.Println("Digite o ano:")
			fmt.Scanln(&ano)
			fmt.Println("Digite o semestre:")
			fmt.Scanln(&semestre)
			// Cria novo objeto de Request para receber lista de alunos
			newRequestAlunos := &classes.AlunoRequest{
				CodDisciplina: codDisciplina,
				Ano:           ano,
				Semestre:      semestre,
			}

			// Envia objeto para receber lista de alunos
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

		// Se o comando for getDisciplinas, envia requisição para receber lista de disciplinas, passando ano e semestre
		if input == "getDisciplinas" {
			// Recebe input do usuário para dados
			var ano int32
			var semestre int32
			fmt.Println("Digite o ano:")
			fmt.Scanln(&ano)
			fmt.Println("Digite o semestre:")
			fmt.Scanln(&semestre)
			// Cria novo objeto de Request para receber lista de disciplinas
			newRequestDisciplinas := &classes.DisciplinaRequest{
				Ano:      ano,
				Semestre: semestre,
			}

			// Envia objeto para receber lista de disciplinas
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

		// Se o comando for sair, encerra o programa
		if input == "sair" {
			break
		}
	}
}
