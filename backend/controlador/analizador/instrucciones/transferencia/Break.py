from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Break(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)

    def getNodo(self):
        nodo = NodoAST('BREAK')
        nodo.agregar('break')
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        return 'ByLy23'
