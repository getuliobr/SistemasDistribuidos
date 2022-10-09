package main

import (
	classes "Client/classes"
	"fmt"

	"google.golang.org/protobuf/proto"
)

func main() {
	curso := &classes.Curso{
		Id:   1,
		Nome: "Curso de Go",
	}

	c , err := proto.Marshal(curso)
	if err != nil {
		fmt.Println("Erro ao serializar o objeto")
	}

	var u classes.Curso
	err1 := proto.Unmarshal(c, &u)
	if err1 != nil {
		fmt.Println("Erro ao desserializar o objeto")
	}
	fmt.Println(u.Id)
	fmt.Println(u.Nome)
}
