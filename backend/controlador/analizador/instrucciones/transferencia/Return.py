from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Return(Instruccion):
    valor = None

    def __init__(self, linea, columna, expresion=None):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.expresion = expresion

    def traducir(self, arbol, tablaSimbolo):  # pendiente
        if self.expresion != None:
            self.valor = self.expresion.traducir(arbol, tablaSimbolo)
            self.tipo = self.expresion.tipo
            self.tipoStruct = self.expresion.tipoStruct
            self.mutable = self.expresion.mutable
        return self

    def getNodo(self):
        nodo = NodoAST('RETURN')
        nodo.agregar('return')
        if self.expresion != None:
            nodo.agregarAST(self.expresion.getNodo())
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        if self.expresion != None:
            self.valor = self.expresion.interpretar(arbol, tablaSimbolo)
            self.tipo = self.expresion.tipo
            self.tipoStruct = self.expresion.tipoStruct
            self.mutable = self.expresion.mutable
        return self
