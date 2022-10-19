import Pyro5.api

@Pyro5.api.expose
class CalcService:
    def soma(self, a, b):
        return a + b
    
    def subtracao(self, a, b):
        return a - b