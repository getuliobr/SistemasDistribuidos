import Pyro5.server, Pyro5.api
from calc import Calculadora
from agenda import Agenda

daemon = Pyro5.server.Daemon()
uri = daemon.register(Calculadora)
ns = Pyro5.api.locate_ns()
ns.register("CalcService", uri)

uri = daemon.register(Agenda)
ns = Pyro5.api.locate_ns()
ns.register("AgendaService", uri)
daemon.requestLoop()