from optimizador.analizador.abstracto.Instruccion import Instruccion


class Encabezado(Instruccion):
    def __init__(self, lista, linea, columna):
        super().__init__(linea, columna)
        self.lista = lista

    def getInstruccion(self, arbol):
        for i in self.lista:
            print(i)
