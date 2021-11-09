from optimizador.analizador.abstracto.Instruccion import Instruccion


class Mod(Instruccion):
    def __init__(self, temp, t1, t2, linea, columna):
        super().__init__(linea, columna)
        self.temp = temp
        self.t1 = t1
        self.t2 = t2

    def getInstruccion(self, arbol):
        return '{} = math.Mod({},{});\n'.format(self.temp, self.t1, self.t2)

    def getNormal(self):
        return '{} = math.Mod({},{});\n'.format(
            self.temp, self.t1, self.t2)
