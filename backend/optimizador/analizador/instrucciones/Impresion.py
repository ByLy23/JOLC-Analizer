from optimizador.analizador.abstracto.Instruccion import Instruccion


class Impresion(Instruccion):
    def __init__(self, tipo, terminal, linea, columna):
        super().__init__(linea, columna)
        self.tipo = tipo
        self.terminal = terminal

    def getInstruccion(self, arbol):
        return 'fmt.Printf("{}", int({}));\n'.format(self.tipo, self.terminal)

    def getNormal(self):
        return 'fmt.Printf("{}", int({}));\n'.format(self.tipo, self.terminal)
