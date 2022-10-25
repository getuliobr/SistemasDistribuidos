import random
import Pyro5.api

nameserver = Pyro5.api.locate_ns()
uri = nameserver.lookup("CalcService")

calc_proxy = Pyro5.api.Proxy(uri)
print(calc_proxy.soma(10, 20))
print(calc_proxy.subtracao(10, 20))

uri = nameserver.lookup("AgendaService")
agenda_proxy = Pyro5.api.Proxy(uri)

nome = input("Digite o nome do contato: ")
telefone = input("Digite o telefone do contato: ")
agenda_proxy.adicionar(nome, telefone)
print(agenda_proxy.listar())


print(agenda_proxy.buscar(nome))
print(agenda_proxy.buscar('naoexiste12323123'))

print(agenda_proxy.atualizar(nome, '123456789'))
print(agenda_proxy.listar())

agenda_proxy.remover(nome)
print(agenda_proxy.listar())