import Pyro5.server, Pyro5.api
from calc import CalcService

daemon = Pyro5.server.Daemon()
uri = daemon.register(CalcService)
ns = Pyro5.api.locate_ns()
ns.register("CalcService", uri)
daemon.requestLoop()