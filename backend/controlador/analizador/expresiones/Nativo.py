from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Nativo(Instruccion):
    def __init__(self, tipo, valor, linea, columna):
        super().__init__(tipo, linea, columna)
        self.valor = valor

    def getNodo(self):
        nodo = NodoAST('NATIVO')
        nodo.agregar(self.valor)
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        return self.valor
