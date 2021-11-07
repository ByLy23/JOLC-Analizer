from optimizador.analizador.abstracto.Instruccion import Instruccion


class Return(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def getInstruccion(self, arbol):
        return 'return;'

    def getNormal(self):
        return 'return;'
