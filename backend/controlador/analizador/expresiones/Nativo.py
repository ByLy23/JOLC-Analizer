from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Nativo(Instruccion):
    def __init__(self, tipo, valor, linea, columna):
        super().__init__(tipo, linea, columna)
        self.valor = valor
        self.temporal = valor

    def getNodo(self):
        nodo = NodoAST('NATIVO')
        nodo.agregar(self.valor)
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        return self.valor

    def traducir(self, arbol, tablaSimbolo):
        if(self.tipo == TipoDato.BOOLEANO):
            if self.temporal:
                self.temporal = 1.0
            else:
                self.temporal = 0.0
        elif self.tipo == TipoDato.NOTHING:
            self.temporal = -50251313792.0
        elif self.temporal == TipoDato.ENTERO:
            self.temporal = float(self.valor)
        elif self.temporal == TipoDato.CARACTER:
            self.temporal = float(ord(self.valor))
        return arbol.nuevoTemp(str(self.temporal))
        #resultado = {'temporal': self.temporal, 'codigo': ""}
