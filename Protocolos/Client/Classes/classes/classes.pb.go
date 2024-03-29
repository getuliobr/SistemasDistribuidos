// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.28.1
// 	protoc        v3.21.7
// source: classes.proto

package classes

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type Aluno struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	RA       int32  `protobuf:"varint,1,opt,name=RA,proto3" json:"RA,omitempty"`
	Nome     string `protobuf:"bytes,2,opt,name=Nome,proto3" json:"Nome,omitempty"`
	Periodo  int32  `protobuf:"varint,3,opt,name=Periodo,proto3" json:"Periodo,omitempty"`
	CodCurso int32  `protobuf:"varint,4,opt,name=Cod_curso,json=CodCurso,proto3" json:"Cod_curso,omitempty"`
}

func (x *Aluno) Reset() {
	*x = Aluno{}
	if protoimpl.UnsafeEnabled {
		mi := &file_classes_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Aluno) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Aluno) ProtoMessage() {}

func (x *Aluno) ProtoReflect() protoreflect.Message {
	mi := &file_classes_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Aluno.ProtoReflect.Descriptor instead.
func (*Aluno) Descriptor() ([]byte, []int) {
	return file_classes_proto_rawDescGZIP(), []int{0}
}

func (x *Aluno) GetRA() int32 {
	if x != nil {
		return x.RA
	}
	return 0
}

func (x *Aluno) GetNome() string {
	if x != nil {
		return x.Nome
	}
	return ""
}

func (x *Aluno) GetPeriodo() int32 {
	if x != nil {
		return x.Periodo
	}
	return 0
}

func (x *Aluno) GetCodCurso() int32 {
	if x != nil {
		return x.CodCurso
	}
	return 0
}

type Curso struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Id   int32  `protobuf:"varint,1,opt,name=Id,proto3" json:"Id,omitempty"`
	Nome string `protobuf:"bytes,2,opt,name=Nome,proto3" json:"Nome,omitempty"`
}

func (x *Curso) Reset() {
	*x = Curso{}
	if protoimpl.UnsafeEnabled {
		mi := &file_classes_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Curso) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Curso) ProtoMessage() {}

func (x *Curso) ProtoReflect() protoreflect.Message {
	mi := &file_classes_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Curso.ProtoReflect.Descriptor instead.
func (*Curso) Descriptor() ([]byte, []int) {
	return file_classes_proto_rawDescGZIP(), []int{1}
}

func (x *Curso) GetId() int32 {
	if x != nil {
		return x.Id
	}
	return 0
}

func (x *Curso) GetNome() string {
	if x != nil {
		return x.Nome
	}
	return ""
}

type Disciplina struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Codigo    string `protobuf:"bytes,1,opt,name=Codigo,proto3" json:"Codigo,omitempty"`
	Nome      string `protobuf:"bytes,2,opt,name=Nome,proto3" json:"Nome,omitempty"`
	Professor string `protobuf:"bytes,3,opt,name=Professor,proto3" json:"Professor,omitempty"`
	CodCurso  int32  `protobuf:"varint,4,opt,name=Cod_curso,json=CodCurso,proto3" json:"Cod_curso,omitempty"`
}

func (x *Disciplina) Reset() {
	*x = Disciplina{}
	if protoimpl.UnsafeEnabled {
		mi := &file_classes_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Disciplina) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Disciplina) ProtoMessage() {}

func (x *Disciplina) ProtoReflect() protoreflect.Message {
	mi := &file_classes_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Disciplina.ProtoReflect.Descriptor instead.
func (*Disciplina) Descriptor() ([]byte, []int) {
	return file_classes_proto_rawDescGZIP(), []int{2}
}

func (x *Disciplina) GetCodigo() string {
	if x != nil {
		return x.Codigo
	}
	return ""
}

func (x *Disciplina) GetNome() string {
	if x != nil {
		return x.Nome
	}
	return ""
}

func (x *Disciplina) GetProfessor() string {
	if x != nil {
		return x.Professor
	}
	return ""
}

func (x *Disciplina) GetCodCurso() int32 {
	if x != nil {
		return x.CodCurso
	}
	return 0
}

type Matricula struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	RA            int32   `protobuf:"varint,1,opt,name=RA,proto3" json:"RA,omitempty"`
	CodDisciplina string  `protobuf:"bytes,2,opt,name=Cod_disciplina,json=CodDisciplina,proto3" json:"Cod_disciplina,omitempty"`
	Ano           int32   `protobuf:"varint,3,opt,name=Ano,proto3" json:"Ano,omitempty"`
	Semestre      int32   `protobuf:"varint,4,opt,name=Semestre,proto3" json:"Semestre,omitempty"`
	Nota          float32 `protobuf:"fixed32,5,opt,name=Nota,proto3" json:"Nota,omitempty"`
	Faltas        int32   `protobuf:"varint,6,opt,name=Faltas,proto3" json:"Faltas,omitempty"`
}

func (x *Matricula) Reset() {
	*x = Matricula{}
	if protoimpl.UnsafeEnabled {
		mi := &file_classes_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Matricula) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Matricula) ProtoMessage() {}

func (x *Matricula) ProtoReflect() protoreflect.Message {
	mi := &file_classes_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Matricula.ProtoReflect.Descriptor instead.
func (*Matricula) Descriptor() ([]byte, []int) {
	return file_classes_proto_rawDescGZIP(), []int{3}
}

func (x *Matricula) GetRA() int32 {
	if x != nil {
		return x.RA
	}
	return 0
}

func (x *Matricula) GetCodDisciplina() string {
	if x != nil {
		return x.CodDisciplina
	}
	return ""
}

func (x *Matricula) GetAno() int32 {
	if x != nil {
		return x.Ano
	}
	return 0
}

func (x *Matricula) GetSemestre() int32 {
	if x != nil {
		return x.Semestre
	}
	return 0
}

func (x *Matricula) GetNota() float32 {
	if x != nil {
		return x.Nota
	}
	return 0
}

func (x *Matricula) GetFaltas() int32 {
	if x != nil {
		return x.Faltas
	}
	return 0
}

var File_classes_proto protoreflect.FileDescriptor

var file_classes_proto_rawDesc = []byte{
	0x0a, 0x0d, 0x63, 0x6c, 0x61, 0x73, 0x73, 0x65, 0x73, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22,
	0x62, 0x0a, 0x05, 0x41, 0x6c, 0x75, 0x6e, 0x6f, 0x12, 0x0e, 0x0a, 0x02, 0x52, 0x41, 0x18, 0x01,
	0x20, 0x01, 0x28, 0x05, 0x52, 0x02, 0x52, 0x41, 0x12, 0x12, 0x0a, 0x04, 0x4e, 0x6f, 0x6d, 0x65,
	0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x4e, 0x6f, 0x6d, 0x65, 0x12, 0x18, 0x0a, 0x07,
	0x50, 0x65, 0x72, 0x69, 0x6f, 0x64, 0x6f, 0x18, 0x03, 0x20, 0x01, 0x28, 0x05, 0x52, 0x07, 0x50,
	0x65, 0x72, 0x69, 0x6f, 0x64, 0x6f, 0x12, 0x1b, 0x0a, 0x09, 0x43, 0x6f, 0x64, 0x5f, 0x63, 0x75,
	0x72, 0x73, 0x6f, 0x18, 0x04, 0x20, 0x01, 0x28, 0x05, 0x52, 0x08, 0x43, 0x6f, 0x64, 0x43, 0x75,
	0x72, 0x73, 0x6f, 0x22, 0x2b, 0x0a, 0x05, 0x43, 0x75, 0x72, 0x73, 0x6f, 0x12, 0x0e, 0x0a, 0x02,
	0x49, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52, 0x02, 0x49, 0x64, 0x12, 0x12, 0x0a, 0x04,
	0x4e, 0x6f, 0x6d, 0x65, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x4e, 0x6f, 0x6d, 0x65,
	0x22, 0x73, 0x0a, 0x0a, 0x44, 0x69, 0x73, 0x63, 0x69, 0x70, 0x6c, 0x69, 0x6e, 0x61, 0x12, 0x16,
	0x0a, 0x06, 0x43, 0x6f, 0x64, 0x69, 0x67, 0x6f, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x06,
	0x43, 0x6f, 0x64, 0x69, 0x67, 0x6f, 0x12, 0x12, 0x0a, 0x04, 0x4e, 0x6f, 0x6d, 0x65, 0x18, 0x02,
	0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x4e, 0x6f, 0x6d, 0x65, 0x12, 0x1c, 0x0a, 0x09, 0x50, 0x72,
	0x6f, 0x66, 0x65, 0x73, 0x73, 0x6f, 0x72, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52, 0x09, 0x50,
	0x72, 0x6f, 0x66, 0x65, 0x73, 0x73, 0x6f, 0x72, 0x12, 0x1b, 0x0a, 0x09, 0x43, 0x6f, 0x64, 0x5f,
	0x63, 0x75, 0x72, 0x73, 0x6f, 0x18, 0x04, 0x20, 0x01, 0x28, 0x05, 0x52, 0x08, 0x43, 0x6f, 0x64,
	0x43, 0x75, 0x72, 0x73, 0x6f, 0x22, 0x9c, 0x01, 0x0a, 0x09, 0x4d, 0x61, 0x74, 0x72, 0x69, 0x63,
	0x75, 0x6c, 0x61, 0x12, 0x0e, 0x0a, 0x02, 0x52, 0x41, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52,
	0x02, 0x52, 0x41, 0x12, 0x25, 0x0a, 0x0e, 0x43, 0x6f, 0x64, 0x5f, 0x64, 0x69, 0x73, 0x63, 0x69,
	0x70, 0x6c, 0x69, 0x6e, 0x61, 0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x0d, 0x43, 0x6f, 0x64,
	0x44, 0x69, 0x73, 0x63, 0x69, 0x70, 0x6c, 0x69, 0x6e, 0x61, 0x12, 0x10, 0x0a, 0x03, 0x41, 0x6e,
	0x6f, 0x18, 0x03, 0x20, 0x01, 0x28, 0x05, 0x52, 0x03, 0x41, 0x6e, 0x6f, 0x12, 0x1a, 0x0a, 0x08,
	0x53, 0x65, 0x6d, 0x65, 0x73, 0x74, 0x72, 0x65, 0x18, 0x04, 0x20, 0x01, 0x28, 0x05, 0x52, 0x08,
	0x53, 0x65, 0x6d, 0x65, 0x73, 0x74, 0x72, 0x65, 0x12, 0x12, 0x0a, 0x04, 0x4e, 0x6f, 0x74, 0x61,
	0x18, 0x05, 0x20, 0x01, 0x28, 0x02, 0x52, 0x04, 0x4e, 0x6f, 0x74, 0x61, 0x12, 0x16, 0x0a, 0x06,
	0x46, 0x61, 0x6c, 0x74, 0x61, 0x73, 0x18, 0x06, 0x20, 0x01, 0x28, 0x05, 0x52, 0x06, 0x46, 0x61,
	0x6c, 0x74, 0x61, 0x73, 0x42, 0x0a, 0x5a, 0x08, 0x63, 0x6c, 0x61, 0x73, 0x73, 0x65, 0x73, 0x2f,
	0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_classes_proto_rawDescOnce sync.Once
	file_classes_proto_rawDescData = file_classes_proto_rawDesc
)

func file_classes_proto_rawDescGZIP() []byte {
	file_classes_proto_rawDescOnce.Do(func() {
		file_classes_proto_rawDescData = protoimpl.X.CompressGZIP(file_classes_proto_rawDescData)
	})
	return file_classes_proto_rawDescData
}

var file_classes_proto_msgTypes = make([]protoimpl.MessageInfo, 4)
var file_classes_proto_goTypes = []interface{}{
	(*Aluno)(nil),      // 0: Aluno
	(*Curso)(nil),      // 1: Curso
	(*Disciplina)(nil), // 2: Disciplina
	(*Matricula)(nil),  // 3: Matricula
}
var file_classes_proto_depIdxs = []int32{
	0, // [0:0] is the sub-list for method output_type
	0, // [0:0] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_classes_proto_init() }
func file_classes_proto_init() {
	if File_classes_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_classes_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Aluno); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_classes_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Curso); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_classes_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Disciplina); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_classes_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*Matricula); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_classes_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   4,
			NumExtensions: 0,
			NumServices:   0,
		},
		GoTypes:           file_classes_proto_goTypes,
		DependencyIndexes: file_classes_proto_depIdxs,
		MessageInfos:      file_classes_proto_msgTypes,
	}.Build()
	File_classes_proto = out.File
	file_classes_proto_rawDesc = nil
	file_classes_proto_goTypes = nil
	file_classes_proto_depIdxs = nil
}
