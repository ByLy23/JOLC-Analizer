from optimizador.analizador.abstracto.Instruccion import Instruccion


class Goto(Instruccion):
    def __init__(self, label, linea, columna):
        super().__init__(linea, columna)
        self.label = label

    def getInstruccion(self, arbol):
        etiqueta = self.label.getInstruccion(arbol)
        aux = ""
        for i in etiqueta:
            if i != ":":
                aux += i
            else:
                break
        return 'goto {};\n'.format(aux)

    def getNormal(self):
        return 'goto {};\n'.format(self.label)
