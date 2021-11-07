from optimizador.analizador.abstracto.Instruccion import Instruccion


class ObtenerHeapStack(Instruccion):
    def __init__(self, t1, hs, acceso, linea, columna):
        super().__init__(linea, columna)
        self.t1 = t1
        self.hs = hs
        self.acceso = acceso

    def getInstruccion(self, arbol):
        return '{} = {}[int({})];\n'.format(self.t1, self.hs, self.acceso)

    def getNormal(self):
        return '{} = {}[int({})];\n'.format(self.t1, self.hs, self.acceso)
