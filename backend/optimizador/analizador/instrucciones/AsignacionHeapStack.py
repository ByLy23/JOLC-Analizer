from optimizador.analizador.abstracto.Instruccion import Instruccion


class AsignacionHeapStack(Instruccion):
    def __init__(self, heap_stack, acceso, temp, linea, columna):
        super().__init__(linea, columna)
        self.hs = heap_stack
        self.acceso = acceso
        self.temp = temp

    def getInstruccion(self, arbol):
        return '{}[int( {} ) = {} ];\n'.format(self.hs, self.acceso, self.temp)

    def getNormal(self):
        return '{}[int( {} )] = {};\n'.format(self.hs, self.acceso, self.temp)
