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

// Types of commands
var CREATE int32 = 0x01
var READ int32 = 0x02
var LIST int32 = 0x03
var UPDATE int32 = 0x04
var DELETE int32 = 0x05
var LISTALUNOFROMDISCIPLINA int32 = 0x06
var COMMAND_LISTADNFFROMAS int32 = 0x07

// Types of entities
var CURSO int32 = 0x10
var DISCIPLINA int32 = 0x11
var ALUNO int32 = 0x12
var MATRICULA int32 = 0x13



func input_matricula(conn net.Conn, typeCommand int32) {
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
	if typeCommand == CREATE {
		create_matricula(conn, ra, codDisciplina, ano, semestre, nota, faltas)
	}
	if typeCommand == UPDATE{
		fmt.Println("Digite a nota:")
		fmt.Scanln(&nota)
		fmt.Println("Digite o faltas:")
		fmt.Scanln(&faltas)
		
		update_matricula(conn, ra, codDisciplina, ano, semestre, nota, faltas)
	}
}

func input_aluno(conn net.Conn, typeCommand int32) {
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
	if typeCommand == CREATE {
		create_aluno(conn, ra, nome, periodo, cod_curso)
	}
	if typeCommand == UPDATE{
		update_aluno(conn, ra, nome, periodo, cod_curso)
	}
}

func create_matricula(conn net.Conn, ra int32, codDisciplina string, ano int32, semestre int32, nota float32, faltas int32) {
	// TODO
	newMatricula := &classes.Matricula{
		RA:            ra,
		CodDisciplina: codDisciplina,
		Ano:           ano,
		Semestre:      semestre,
		Nota:          nota,
		Faltas:        faltas,
	}

	matriculaMarshal, err := proto.Marshal(newMatricula)
	if err != nil {
		log.Fatal("marshaling error: ", err)
		return
	}
	binary.Write(conn, binary.LittleEndian, int8(CREATE))
	binary.Write(conn, binary.LittleEndian, int8(MATRICULA))
	binary.Write(conn, binary.LittleEndian, int32(len(matriculaMarshal)))
	conn.Write(matriculaMarshal)
}

func update_matricula(conn net.Conn, ra int32, codDisciplina string, ano int32, semestre int32, nota float32, faltas int32){
	updatedMatricula := &classes.Matricula{
		RA:            ra,
		CodDisciplina: codDisciplina,
		Ano:           ano,
		Semestre:      semestre,
		Nota:          nota,
		Faltas:        faltas,
	}

	matriculaMarshal, err := proto.Marshal(updatedMatricula)
	if err != nil {
		log.Fatal("marshaling error: ", err)
		return
	}
	binary.Write(conn, binary.LittleEndian, int8(UPDATE))
	binary.Write(conn, binary.LittleEndian, int8(MATRICULA))
	binary.Write(conn, binary.LittleEndian, int32(len(matriculaMarshal)))
	conn.Write(matriculaMarshal)
}

func list_matricula(conn net.Conn) {
	binary.Write(conn, binary.LittleEndian, int8(LIST))
	binary.Write(conn, binary.LittleEndian, int8(MATRICULA))

	buffer := make([]byte, 4)
	conn.Read(buffer)
	size := binary.LittleEndian.Uint32(buffer)
	
	fmt.Println("--------------------")
	for i := uint32(0); i < size; i ++ {
		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeMatricula := binary.LittleEndian.Uint32(buffer)
		buffer = make([]byte, sizeMatricula)
		conn.Read(buffer)
		matricula := &classes.Matricula{}
		err := proto.Unmarshal(buffer, matricula)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}
		fmt.Println(matricula)
	}
}

func create_aluno(conn net.Conn, ra int32, nome string, periodo int32, cod_curso int32) {
	newAluno := &classes.Aluno{
		RA:       ra,
		Nome:     nome,
		Periodo:  periodo,
		CodCurso: cod_curso,
	}

	alunoMarshal, err := proto.Marshal(newAluno)
	if err != nil {
		log.Fatal("marshaling error: ", err)
		return
	}
	binary.Write(conn, binary.LittleEndian, int8(CREATE))
	binary.Write(conn, binary.LittleEndian, int8(ALUNO))
	binary.Write(conn, binary.LittleEndian, int32(len(alunoMarshal)))
	conn.Write(alunoMarshal)
}

func update_aluno(conn net.Conn, ra int32, nome string, periodo int32, cod_curso int32){
	updatedAluno := &classes.Aluno{
		RA:       ra,
		Nome:     nome,
		Periodo:  periodo,
		CodCurso: cod_curso,
	}

	alunoMarshal, err := proto.Marshal(updatedAluno)
	if err != nil {
		log.Fatal("marshaling error: ", err)
		return
	}
	binary.Write(conn, binary.LittleEndian, int8(UPDATE))
	binary.Write(conn, binary.LittleEndian, int8(ALUNO))
	binary.Write(conn, binary.LittleEndian, int32(len(alunoMarshal)))
	conn.Write(alunoMarshal)
}

func list_aluno(conn net.Conn) {
	fmt.Println("Digite o Disciplina:")
	var codDisciplina string
	fmt.Scanln(&codDisciplina)
	fmt.Println("Digite o Ano:")
	var ano int32
	fmt.Scanln(&ano)
	fmt.Println("Digite o Semestre:")
	var semestre int32
	fmt.Scanln(&semestre)
	binary.Write(conn, binary.LittleEndian, int8(LISTALUNOFROMDISCIPLINA))
	binary.Write(conn, binary.LittleEndian, int32(len(codDisciplina)))
	conn.Write([]byte(codDisciplina))
	binary.Write(conn, binary.LittleEndian, ano)
	binary.Write(conn, binary.LittleEndian, semestre)

	buffer := make([]byte, 4)
	conn.Read(buffer)
	size := binary.LittleEndian.Uint32(buffer)
	fmt.Println("--------------------")
	for i := uint32(0); i < size; i ++ {
		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeAluno := binary.LittleEndian.Uint32(buffer)
		buffer = make([]byte, sizeAluno)
		conn.Read(buffer)
		aluno := &classes.Aluno{}
		err := proto.Unmarshal(buffer, aluno)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}
		fmt.Println(aluno)
	}

}

//TODO
func list_disciplina(conn net.Conn){
	fmt.Println("Digite o Ano:")
	var ano int32
	fmt.Scanln(&ano)
	fmt.Println("Digite o Semestre:")
	var semestre int32
	fmt.Scanln(&semestre)
	binary.Write(conn, binary.LittleEndian, int8(COMMAND_LISTADNFFROMAS))
	binary.Write(conn, binary.LittleEndian, ano)
	binary.Write(conn, binary.LittleEndian, semestre)

	buffer := make([]byte, 4)
	conn.Read(buffer)
	size := binary.LittleEndian.Uint32(buffer)
	fmt.Println("--------------------")
	for i := uint32(0); i < size; i ++ {

		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeDisciplina := binary.LittleEndian.Uint32(buffer)
		buffer = make([]byte, sizeDisciplina)
		conn.Read(buffer)
		disciplina := &classes.Disciplina{}
		err := proto.Unmarshal(buffer, disciplina)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}

		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeMatricula := binary.LittleEndian.Uint32(buffer)
		buffer = make([]byte, sizeMatricula)
		conn.Read(buffer)
		matricula := &classes.Matricula{}
		err = proto.Unmarshal(buffer, matricula)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}

		buffer = make([]byte, 4)
		conn.Read(buffer)
		sizeAluno := binary.LittleEndian.Uint32(buffer)
		buffer = make([]byte, sizeAluno)
		conn.Read(buffer)
		aluno := &classes.Aluno{}
		err = proto.Unmarshal(buffer, aluno)
		if err != nil {
			log.Fatal("unmarshaling error: ", err)
		}

		fmt.Printf("|Disciplina: %-3s|RA: %-3d|Aluno: %-3s|Nota: %-3f|Faltas: %-3d|\n",disciplina.GetNome(), aluno.GetRA(), aluno.GetNome(), matricula.GetNota(), matricula.GetFaltas())
	}

}

func main() {

	con, err1 := net.Dial("tcp", "127.0.0.1:6667")
	if err1 != nil {
		log.Println(err1)
		os.Exit(3)
	}

	log.Println("Connected to server")

	for {
		var input string

		fmt.Scanln(&input)

		if input == "exit" {
			os.Exit(0)
		}

		if input == "help" {
			continue
		}

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

		if input == "list" {
			var typeClass string
			fmt.Println("Digite o tipo de classe:")
			fmt.Scanln(&typeClass)
			if strings.Compare(typeClass, "matricula") == 0 {
				list_matricula(con)
			}
			if strings.Compare(typeClass, "aluno") == 0 {
				list_aluno(con)
			}
			if strings.Compare(typeClass, "disciplinas_ano") == 0 {
				list_disciplina(con)
			}
		}

		if input == "update" {
			var typeClass string
			fmt.Println("Digite o tipo de classe:")
			fmt.Scanln(&typeClass)
			if strings.Compare(typeClass, "matricula") == 0 {
				input_matricula(con, UPDATE)
			}
			if strings.Compare(typeClass, "aluno") == 0 {
				input_aluno(con, UPDATE)
			}
		}

		if input == "delete" {
			continue
		}
	}
}
