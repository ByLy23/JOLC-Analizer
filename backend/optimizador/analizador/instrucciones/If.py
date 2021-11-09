from optimizador.analizador.abstracto.Instruccion import Instruccion


class If(Instruccion):
    def __init__(self, op1, rel, op2, label, linea, columna):
        super().__init__(linea, columna)
        self.op1 = op1
        self.rel = rel
        self.op2 = op2
        self.label = label

    def getInstruccion(self, arbol):
        etiqueta = self.label.getInstruccion(arbol)
        aux = ""
        for i in etiqueta:
            if i != ":":
                aux += i
            else:
                break
        return 'if ({} {} {}) goto'.format(self.op1, self.rel, self.op2)+'{'+'{};'.format(aux)+'}\n'

    def getNormal(self):
        return 'if ({} {} {}) goto'.format(self.op1, self.rel, self.op2)+'{'+'{};'.format(self.label)+'}\n'
