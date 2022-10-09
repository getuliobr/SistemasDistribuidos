package main

import (
	"encoding/binary"
	"fmt"
	"log"
	"net"
	"os"
	"strings"

	"Client/classes"

	proto "github.com/golang/protobuf/proto"
)

func input_matricula(conn net.Conn, typeCommand int32){
	var ra int32
	var codDisciplina string
	var ano int32
	var semestre int32
	var nota float32
	var faltas int32
	fmt.Println("Digite o RA:")
	fmt.Scanln(&ra)
	fmt.Println("Digite o codDisciplina:")
	fmt.Scanln(&codDisciplina)
	fmt.Println("Digite o ano:")
	fmt.Scanln(&ano)
	fmt.Println("Digite o semestre:")
	fmt.Scanln(&semestre)
	fmt.Println("Digite o nota:")
	fmt.Scanln(&nota)
	fmt.Println("Digite o faltas:")
	fmt.Scanln(&faltas)
	create_matricula(conn, ra, codDisciplina, ano, semestre, nota, faltas)
}


func create_matricula(conn net.Conn, ra int32, codDisciplina string, ano int32, semestre int32, nota float32, faltas int32) {
	// TODO
	newMatricula := &classes.Matricula{
		RA:         ra,
		CodDisciplina: codDisciplina,
		Ano:        ano,
		Semestre:   semestre,
		Nota:       nota,
		Faltas:     faltas,
	}

	fmt.Println(newMatricula)
	matriculaMarshal := proto.MarshalTextString(newMatricula)
	binary.Write(conn, binary.LittleEndian, int8(0x01))
	binary.Write(conn, binary.LittleEndian, int8(0x13))
	binary.Write(conn, binary.LittleEndian, int32(len(matriculaMarshal)))
	fmt.Fprint(conn, matriculaMarshal)
}
func main() {

	con, err1 := net.Dial("tcp", "127.0.0.1:6666")
	if err1 != nil {
		log.Println(err1)
		os.Exit(3)
	}

	log.Println("Connected to server")

	for{
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
		}
		
		if input == "read"{
			continue
		}

		if input == "update"{
			continue
		}

		if input == "delete"{
			continue
		}
	}
	// curso := &classes.Curso{
	// 	Id:   1,
	// 	Nome: "Curso de Go",
	// }

	// c , err := proto.Marshal(curso)
	// if err != nil {
	// 	fmt.Println("Erro ao serializar o objeto")
	// }

	// var u classes.Curso
	// err1 := proto.Unmarshal(c, &u)
	// if err1 != nil {
	// 	fmt.Println("Erro ao desserializar o objeto")
	// }
	// fmt.Println(u.Id)
	// fmt.Println(u.Nome)
}
