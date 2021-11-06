from optimizador.analizador.abstracto.Instruccion import Instruccion


class Llamada(Instruccion):
    def __init__(self, label, linea, columna):
        super().__init__(linea, columna)
        self.label = label

    def getInstruccion(self, arbol):
        return '{}();\n'.format(self.label)

    def getNormal(self):
        return '{}();\n'.format(self.label)
