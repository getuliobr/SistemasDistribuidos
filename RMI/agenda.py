import Pyro5.api

@Pyro5.api.expose
class Agenda:
    contatos = []

    def adicionar(self, nome, telefone):
        contato = {
            "nome": nome,
            "telefone": telefone
        }
        self.contatos.append(contato)
        return len(self.contatos)

    def listar(self):
        return self.contatos

    def buscar(self, nome):
        for contato in self.contatos:
            if contato['nome'] == nome:
                return contato
        return None

    def remover(self, nome):
        for contato in self.contatos:
            if contato['nome'] == nome:
                self.contatos.remove(contato)
                return True
        return False

    def atualizar(self, nome, telefone):
        for contato in self.contatos:
            if contato['nome'] == nome:
                contato['telefone'] = telefone
                return True
        return False



