/*
		Descrição: Arquivo para abertura de cliente TCP para comunicação e transferência de dados por protocolo (Protobuf)
	    Autores: Getulio Coimbra Regis e Igor Lara de Oliveira
		Creation Date: 18 / 10 / 2022
*/
package main

import (
	"encoding/binary"
	"fmt"
	"log"
	"net"
	"os"
	"strings"

	"Client/classes"

	proto "google.golang.org/protobuf/proto"
)

// Variaveis de comando
var CREATE int32 = 0x01
var READ int32 = 0x02
var LIST int32 = 0x03
var UPDATE int32 = 0x04
var DELETE int32 = 0x05
var LISTALUNOFROMDISCIPLINA int32 = 0x06
var COMMAND_LISTADNFFROMAS int32 = 0x07

// Variaves de entidade
var CURSO int32 = 0x10
var DISCIPLINA int32 = 0x11
var ALUNO int32 = 0x12
var MATRICULA int32 = 0x13


// Função que lida com os inputs da variavel de matricula
func input_matricula(conn net.Conn, typeCommand int32) {
	// Recebe todos os dados de matricula
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

	// Se o comando for de criação, chama a função de criação passando todos os argumentos e a conexão tcp
	if typeCommand == CREATE {
		create_matricula(conn, ra, codDisciplina, ano, semestre, nota, faltas)
	}
	// Se o comando for de update, chama a função de update passando todos os argumentos e a conexão tcp
	if typeCommand == UPDATE{
		fmt.Println("Digite a nota:")
		fmt.Scanln(&nota)
		fmt.Println("Digite o faltas:")
		fmt.Scanln(&faltas)
		
		update_matricula(conn, ra, codDisciplina, ano, semestre, nota, faltas)
	}
}


// Função que lida com os inputs da variavel de aluno
func input_aluno(conn net.Conn, typeCommand int32) {
	// Recebe todos os dados de aluno
	var ra int32
	var nome string
	var periodo int32
	var cod_curso int32
	fmt.Println("Digite o RA:")
	fmt.Scanln(&ra)
	fmt.Println("Digite o nome:")
	fmt.Scanln(&nome)
	fmt.Println("Digite o periodo:")
	fmt.Scanln(&periodo)
	fmt.Println("Digite o cod_curso:")
	fmt.Scanln(&cod_curso)

	// Se o comando for de criação, chama a função de criação passando todos os argumentos e a conexão tcp
	if typeCommand == CREATE {
		create_aluno(conn, ra, nome, periodo, cod_curso)
	}
	// Se o comando for de update, chama a função de update passando todos os argumentos e a conexão tcp
	if typeCommand == UPDATE{
		update_aluno(conn, ra, nome, periodo, cod_curso)
	}
}

// Função que cria matricula
func create_matricula(conn net.Conn, ra int32, codDisciplina string, ano int32, semestre int32, nota float32, faltas int32) {
	
	// Cria objeto de matricula
	newMatricula := &classes.Matricula{
		RA:            ra,
		CodDisciplina: codDisciplina,
		Ano:           ano,
		Semestre:      semestre,
		Nota:          nota,
		Faltas:        faltas,
	}

	// Converte objeto de matricula para bytes
	matriculaMarshal, err := proto.Marshal(newMatricula)
	if err != nil {
		log.Fatal("marshaling error: ", err)
		return
	}
	// Envia comando de criação
	binary.Write(conn, binary.LittleEndian, int8(CREATE))
	// Envia entidade de matricula
	binary.Write(conn, binary.LittleEndian, int8(MATRICULA))
	// Envia tamanho do objeto de matricula
	binary.Write(conn, binary.LittleEndian, int32(len(matriculaMarshal)))
	// Envia objeto de matricula
	conn.Write(matriculaMarshal)
}

// Função que atualiza matricula
func update_matricula(conn net.Conn, ra int32, codDisciplina string, ano int32, semestre int32, nota float32, faltas int32){
	// Cria objeto de matricula
	updatedMatricula := &classes.Matricula{
		RA:            ra,
		CodDisciplina: codDisciplina,
		Ano:           ano,
		Semestre:      semestre,
		Nota:          nota,
		Faltas:        faltas,
	}

	// Converte objeto de matricula para bytes
	matriculaMarshal, err := proto.Marshal(updatedMatricula)
	if err != nil {
		log.Fatal("marshaling error: ", err)
		return
	}

	// Envia comando de update
	binary.Write(conn, binary.LittleEndian, int8(UPDATE))
	// Envia entidade de matricula
	binary.Write(conn, binary.LittleEndian, int8(MATRICULA))
	// Envia tamanho do objeto de matricula
	binary.Write(conn, binary.LittleEndian, int32(len(matriculaMarshal)))
	// Envia objeto de matricula
	conn.Write(matriculaMarshal)
}

// Função que lista matriculas
func list_matricula(conn net.Conn) {
	// Envia comando de listagem
	binary.Write(conn, binary.LittleEndian, int8(LIST))
	// Envia entidade de matricula
	binary.Write(conn, binary.LittleEndian, int8(MATRICULA))

	// Recebe quantidade de matriculas
	buffer := make([]byte, 4)
	conn.Read(buffer)
	size := binary.LittleEndian.Uint32(buffer)
	
	fmt.Println("--------------------")
	// Recebe todas as matriculas
	for i := uint32(0); i < size; i ++ {
		// Recebe tamanho da matricula
		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeMatricula := binary.LittleEndian.Uint32(buffer)

		// Recebe matricula
		buffer = make([]byte, sizeMatricula)
		conn.Read(buffer)

		// Converte matricula para objeto
		matricula := &classes.Matricula{}
		err := proto.Unmarshal(buffer, matricula)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}

		// Imprime matricula
		fmt.Println(matricula)
	}
}

// Função que cria aluno
func create_aluno(conn net.Conn, ra int32, nome string, periodo int32, cod_curso int32) {
	// Cria objeto de aluno
	newAluno := &classes.Aluno{
		RA:       ra,
		Nome:     nome,
		Periodo:  periodo,
		CodCurso: cod_curso,
	}

	// Converte objeto de aluno para bytes
	alunoMarshal, err := proto.Marshal(newAluno)
	if err != nil {
		log.Fatal("marshaling error: ", err)
		return
	}

	// Envia comando de criação
	binary.Write(conn, binary.LittleEndian, int8(CREATE))
	// Envia entidade de aluno
	binary.Write(conn, binary.LittleEndian, int8(ALUNO))
	// Envia tamanho do objeto de aluno
	binary.Write(conn, binary.LittleEndian, int32(len(alunoMarshal)))
	// Envia objeto de aluno
	conn.Write(alunoMarshal)
}

// Função que atualiza aluno
func update_aluno(conn net.Conn, ra int32, nome string, periodo int32, cod_curso int32){
	// Cria objeto de aluno
	updatedAluno := &classes.Aluno{
		RA:       ra,
		Nome:     nome,
		Periodo:  periodo,
		CodCurso: cod_curso,
	}

	// Converte objeto de aluno para bytes
	alunoMarshal, err := proto.Marshal(updatedAluno)
	if err != nil {
		log.Fatal("marshaling error: ", err)
		return
	}
	
	// Envia comando de update
	binary.Write(conn, binary.LittleEndian, int8(UPDATE))
	// Envia entidade de aluno
	binary.Write(conn, binary.LittleEndian, int8(ALUNO))
	// Envia tamanho do objeto de aluno
	binary.Write(conn, binary.LittleEndian, int32(len(alunoMarshal)))
	// Envia objeto de aluno
	conn.Write(alunoMarshal)
}

// Função que lista alunos (RA, nome, período) de uma disciplina informado a disciplina, ano e semestre
func list_aluno(conn net.Conn) {
	// Input da disciplina
	fmt.Println("Digite o Disciplina:") 
	var codDisciplina string
	fmt.Scanln(&codDisciplina)
	// Input do ano
	fmt.Println("Digite o Ano:")
	var ano int32
	fmt.Scanln(&ano)
	// Input do semestre
	fmt.Println("Digite o Semestre:")
	var semestre int32
	fmt.Scanln(&semestre)

	// Envia requisição de ListagemDeAlunoPorDisciplina
	binary.Write(conn, binary.LittleEndian, int8(LISTALUNOFROMDISCIPLINA))

	// Envia tamanho do codigo da disciplina
	binary.Write(conn, binary.LittleEndian, int32(len(codDisciplina)))
	// Envia codigo da disciplina
	conn.Write([]byte(codDisciplina))

	// Envia ano
	binary.Write(conn, binary.LittleEndian, ano)
	// Envia semestre
	binary.Write(conn, binary.LittleEndian, semestre)

	// Recebe quantidade de alunos
	buffer := make([]byte, 4)
	conn.Read(buffer)
	size := binary.LittleEndian.Uint32(buffer)


	fmt.Println("--------------------")
	// Recebe todos os alunos
	for i := uint32(0); i < size; i ++ {
		// Recebe tamanho do aluno
		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeAluno := binary.LittleEndian.Uint32(buffer)

		// Recebe aluno
		buffer = make([]byte, sizeAluno)
		conn.Read(buffer)

		// Converte aluno para objeto
		aluno := &classes.Aluno{}
		err := proto.Unmarshal(buffer, aluno)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}

		// Imprime aluno
		fmt.Println(aluno)
	}

}

// Função que lista disciplinas, faltas e notas (RA, nome, nota, faltas) de um aluno informado o ano e semestre
func list_disciplina(conn net.Conn){
	// Input do Ano
	fmt.Println("Digite o Ano:")
	var ano int32
	fmt.Scanln(&ano)

	// Input do Semestre
	fmt.Println("Digite o Semestre:")
	var semestre int32
	fmt.Scanln(&semestre)

	// Envia requisição de ListagemDeDisciplinasNotasEFaltasFromAnoESemestre
	binary.Write(conn, binary.LittleEndian, int8(COMMAND_LISTADNFFROMAS))
	// Envia ano
	binary.Write(conn, binary.LittleEndian, ano)
	// Envia semestre
	binary.Write(conn, binary.LittleEndian, semestre)

	// Recebe quantidade de disciplinas
	buffer := make([]byte, 4)
	conn.Read(buffer)
	size := binary.LittleEndian.Uint32(buffer)

	fmt.Println("--------------------")
	// Recebe todas as disciplinas
	for i := uint32(0); i < size; i ++ {

		// Recebe tamanho da disciplina
		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeDisciplina := binary.LittleEndian.Uint32(buffer)

		// Recebe disciplina
		buffer = make([]byte, sizeDisciplina)
		conn.Read(buffer)

		// Converte disciplina para objeto
		disciplina := &classes.Disciplina{}
		err := proto.Unmarshal(buffer, disciplina)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}

		// Recebe tamanho de matricula
		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeMatricula := binary.LittleEndian.Uint32(buffer)

		// Recebe matricula
		buffer = make([]byte, sizeMatricula)
		conn.Read(buffer)

		// Converte matricula para objeto
		matricula := &classes.Matricula{}
		err = proto.Unmarshal(buffer, matricula)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}
		
		// Recebe tamanho de aluno
		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeAluno := binary.LittleEndian.Uint32(buffer)

		// Recebe aluno
		buffer = make([]byte, sizeAluno)
		conn.Read(buffer)

		// Converte aluno para objeto
		aluno := &classes.Aluno{}
		err = proto.Unmarshal(buffer, aluno)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}

		// Imprime Disciplina matriculada, RA, Aluno, Nota e Faltas
		fmt.Printf("|Disciplina: %-3s|RA: %-3d|Aluno: %-3s|Nota: %-3f|Faltas: %-3d|\n",disciplina.GetNome(), aluno.GetRA(), aluno.GetNome(), matricula.GetNota(), matricula.GetFaltas())
	}

}

func main() {

	con, err1 := net.Dial("tcp", "127.0.0.1:6667") // Conecta ao servidor
	if err1 != nil {
		log.Println(err1)
		os.Exit(3)
	}

	log.Println("Connected to server") //Log de conexão ao servidor

	for {
		var input string // Lê Input do usuário
		fmt.Scanln(&input) 

		// Se o comando for exit, encerra a conexão
		if input == "exit" {
			os.Exit(0)
		}

		// Se o comando for help, lista os comandos (Não funcional)
		if input == "help" {
			continue
		}

		// Se o comando for create, pede o input da classe e chama a função de criação
		if strings.Compare(input, "create") == 0 {
			var typeClass string
			fmt.Println("Digite o tipo de classe:")
			fmt.Scanln(&typeClass)
			if strings.Compare(typeClass, "matricula") == 0 {
				input_matricula(con, 0x01)
			}
			if strings.Compare(typeClass, "aluno") == 0 {
				input_aluno(con, 0x01)
			}
		}

		// Se o comando for list
		if input == "list" {
			// Input da classe
			var typeClass string
			fmt.Println("Digite o tipo de classe:")
			fmt.Scanln(&typeClass)

			// Lista matriculas
			if strings.Compare(typeClass, "matricula") == 0 {
				list_matricula(con)
			}
			// Lista alunos (RA, nome, período) de uma disciplina informado a disciplina, ano e semestre
			if strings.Compare(typeClass, "aluno") == 0 {
				list_aluno(con)
			}
			// Lista disciplinas, faltas e notas (RA, nome, nota, faltas) de um aluno informado o ano e semestre
			if strings.Compare(typeClass, "disciplinas_ano") == 0 {
				list_disciplina(con)
			}
		}

		// Se o comando for update
		if input == "update" {
			// Input da classe
			var typeClass string
			fmt.Println("Digite o tipo de classe:")
			fmt.Scanln(&typeClass)
			// Atualiza matricula
			if strings.Compare(typeClass, "matricula") == 0 {
				input_matricula(con, UPDATE)
			}
			// Atualiza aluno
			if strings.Compare(typeClass, "aluno") == 0 {
				input_aluno(con, UPDATE)
			}
		}

		// Se o comando for delete, deleta (Não funcional)
		if input == "delete" {
			continue
		}
	}
}
