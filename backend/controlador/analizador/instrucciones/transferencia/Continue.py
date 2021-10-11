from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Continue(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)

    def getNodo(self):
        nodo = NodoAST('CONTINUE')
        nodo.agregar('continue')
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        return 'ByLyContinue'
