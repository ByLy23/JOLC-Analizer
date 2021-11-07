from optimizador.analizador.abstracto.Instruccion import Instruccion


class AsignacionSimple(Instruccion):
    def __init__(self, t1, t2, linea, columna):
        super().__init__(linea, columna)
        self.t1 = t1
        self.t2 = t2

    def getInstruccion(self, arbol):
        return '{} = {};\n'.format(self.t1, self.t2)

    def getNormal(self):
        return '{} = {};\n'.format(self.t1, self.t2)
