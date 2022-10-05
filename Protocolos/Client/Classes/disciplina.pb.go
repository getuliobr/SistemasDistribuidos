// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.28.1
// 	protoc        v3.21.7
// source: disciplina.proto

package Classes

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

type Disciplina struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Codigo    string `protobuf:"bytes,1,opt,name=codigo,proto3" json:"codigo,omitempty"`
	Nome      string `protobuf:"bytes,2,opt,name=nome,proto3" json:"nome,omitempty"`
	Professor string `protobuf:"bytes,3,opt,name=professor,proto3" json:"professor,omitempty"`
	CodCurso  int32  `protobuf:"varint,4,opt,name=cod_curso,json=codCurso,proto3" json:"cod_curso,omitempty"`
}

func (x *Disciplina) Reset() {
	*x = Disciplina{}
	if protoimpl.UnsafeEnabled {
		mi := &file_disciplina_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Disciplina) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Disciplina) ProtoMessage() {}

func (x *Disciplina) ProtoReflect() protoreflect.Message {
	mi := &file_disciplina_proto_msgTypes[0]
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
	return file_disciplina_proto_rawDescGZIP(), []int{0}
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

var File_disciplina_proto protoreflect.FileDescriptor

var file_disciplina_proto_rawDesc = []byte{
	0x0a, 0x10, 0x64, 0x69, 0x73, 0x63, 0x69, 0x70, 0x6c, 0x69, 0x6e, 0x61, 0x2e, 0x70, 0x72, 0x6f,
	0x74, 0x6f, 0x22, 0x73, 0x0a, 0x0a, 0x44, 0x69, 0x73, 0x63, 0x69, 0x70, 0x6c, 0x69, 0x6e, 0x61,
	0x12, 0x16, 0x0a, 0x06, 0x63, 0x6f, 0x64, 0x69, 0x67, 0x6f, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09,
	0x52, 0x06, 0x63, 0x6f, 0x64, 0x69, 0x67, 0x6f, 0x12, 0x12, 0x0a, 0x04, 0x6e, 0x6f, 0x6d, 0x65,
	0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x52, 0x04, 0x6e, 0x6f, 0x6d, 0x65, 0x12, 0x1c, 0x0a, 0x09,
	0x70, 0x72, 0x6f, 0x66, 0x65, 0x73, 0x73, 0x6f, 0x72, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x52,
	0x09, 0x70, 0x72, 0x6f, 0x66, 0x65, 0x73, 0x73, 0x6f, 0x72, 0x12, 0x1b, 0x0a, 0x09, 0x63, 0x6f,
	0x64, 0x5f, 0x63, 0x75, 0x72, 0x73, 0x6f, 0x18, 0x04, 0x20, 0x01, 0x28, 0x05, 0x52, 0x08, 0x63,
	0x6f, 0x64, 0x43, 0x75, 0x72, 0x73, 0x6f, 0x42, 0x0b, 0x5a, 0x09, 0x2e, 0x2f, 0x43, 0x6c, 0x61,
	0x73, 0x73, 0x65, 0x73, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_disciplina_proto_rawDescOnce sync.Once
	file_disciplina_proto_rawDescData = file_disciplina_proto_rawDesc
)

func file_disciplina_proto_rawDescGZIP() []byte {
	file_disciplina_proto_rawDescOnce.Do(func() {
		file_disciplina_proto_rawDescData = protoimpl.X.CompressGZIP(file_disciplina_proto_rawDescData)
	})
	return file_disciplina_proto_rawDescData
}

var file_disciplina_proto_msgTypes = make([]protoimpl.MessageInfo, 1)
var file_disciplina_proto_goTypes = []interface{}{
	(*Disciplina)(nil), // 0: Disciplina
}
var file_disciplina_proto_depIdxs = []int32{
	0, // [0:0] is the sub-list for method output_type
	0, // [0:0] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_disciplina_proto_init() }
func file_disciplina_proto_init() {
	if File_disciplina_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_disciplina_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
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
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_disciplina_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   1,
			NumExtensions: 0,
			NumServices:   0,
		},
		GoTypes:           file_disciplina_proto_goTypes,
		DependencyIndexes: file_disciplina_proto_depIdxs,
		MessageInfos:      file_disciplina_proto_msgTypes,
	}.Build()
	File_disciplina_proto = out.File
	file_disciplina_proto_rawDesc = nil
	file_disciplina_proto_goTypes = nil
	file_disciplina_proto_depIdxs = nil
}
