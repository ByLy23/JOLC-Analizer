class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.optimizacion = []

    def getReporte(self):
        return self.optimizacion

    def getInstrucciones(self):
        return self.instrucciones
