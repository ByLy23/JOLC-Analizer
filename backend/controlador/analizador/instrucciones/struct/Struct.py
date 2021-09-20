from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Struct(Instruccion):
    def __init__(self, mutable, identificador, parametros, linea, columna):
        super().__init__(TipoDato.STRUCT, linea, columna)
        self.mutable = mutable
        self.identificador = identificador
        self.parametros = parametros

    def getNodo(self):
        nodo = NodoAST('STRUCT')
        if self.mutable:
            nodo.agregar('mutable')
        nodo.agregar('struct')
        nodo.agregar(self.identificador)
        for param in self.parametros:
            if param["tipato"] != None:
                nodo.agregar(param["identificador"])
                nodo.agregar(':')
                nodo.agregar(':')
                nodo.agregar(param["tipato"])
            else:
                nodo.agregar(param["identificador"])
            nodo.agregar(';')
        nodo.agregar('end')
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        arbol.getStructs().append(self)
