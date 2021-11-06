from abc import abstractmethod


class Instruccion:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

    @abstractmethod
    def getInstruccion(self, arbol):
        pass

    @abstractmethod
    def getNormal(self):
        pass
