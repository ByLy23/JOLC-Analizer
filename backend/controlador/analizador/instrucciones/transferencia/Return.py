from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Return(Instruccion):
    valor = None

    def __init__(self, linea, columna, expresion=None):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.expresion = expresion

    def interpretar(self, arbol, tablaSimbolo):
        if self.expresion != None:
            self.valor = self.expresion.interpretar(arbol, tablaSimbolo)
            self.tipo = self.expresion.tipo
            self.tipoStruct = self.expresion.tipoStruct
            # print(self.expresion.tipo)
        return self
