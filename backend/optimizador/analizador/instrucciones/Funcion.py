from optimizador.analizador.abstracto.Instruccion import Instruccion


class Funcion(Instruccion):
    def __init__(self, ide, linea, columna):
        super().__init__(linea, columna)
        self.ide = ide

    def getInstruccion(self, arbol):
        return self.ide+'();\n'

    def getNormal(self):
        return self.ide+'();\n'
