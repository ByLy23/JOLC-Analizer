from controlador.analizador.abstracto.Instruccion import Instruccion
from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.Tipo import TipoDato


class Comentarios(Instruccion):
    def __init__(self, comentario, multilinea, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.comentario = comentario
        self.multilinea = multilinea

    def traducir(self, arbol, tablaSimbolo):
        print(self.multilinea)
        codigo = ""
        if self.multilinea:
            comm = self.comentario
            print(comm)
            codigo += "/*"+comm+"*/"
        else:
            comm = self.comentario[1:]
            print(comm[1:])
            codigo += "//"+comm

        return {'codigo': codigo}

    def getNodo(self):
        nodo = NodoAST('COMENTARIO')
        if self.multilinea:
            nodo.agregar('//')
            nodo.agregar(self.comentario)
        else:
            nodo.agregar('/*')
            nodo.agregar(self.comentario)
            nodo.agregar('*/')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        return None
