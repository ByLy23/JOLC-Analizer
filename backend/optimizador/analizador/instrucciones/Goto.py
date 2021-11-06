from optimizador.analizador.abstracto.Instruccion import Instruccion


class Goto(Instruccion):
    def __init__(self, label, linea, columna):
        super().__init__(linea, columna)
        self.label = label

    def getInstruccion(self, arbol):
        return 'goto {};\n'.format(self.label)

    def getNormal(self):
        return 'goto {};\n'.format(self.label)
