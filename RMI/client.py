import Pyro5.api

nameserver = Pyro5.api.locate_ns()
uri = nameserver.lookup("CalcService")

calc_proxy = Pyro5.api.Proxy(uri)
print(calc_proxy.soma(10, 20))
print(calc_proxy.subtracao(10, 20))