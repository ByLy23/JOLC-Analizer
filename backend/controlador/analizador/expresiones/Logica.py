from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato, opLogico
from controlador.analizador.abstracto.Instruccion import Instruccion


class Logica(Instruccion):
    def __init__(self, relacion, linea, columna, cond1, cond2=None):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.relacion = relacion
        self.cond1 = cond1
        self.condExcep = None
        if cond2 == None:
            self.condExcep = cond1
        else:
            self.cond1 = cond1
            self.cond2 = cond2

    def getNodo(self):
        nodo = NodoAST('LOGICA')
        if self.condExcep != None:
            nodo.agregar(self.relacion, 'log', self.relacion)
            nodo.agregar(self.condExcep.getNodo())
        else:
            nodo.agregar(self.cond1.getNodo())
            nodo.agregar(self.relacion, 'log', self.relacion)
            nodo.agregar(self.cond2)
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        izq = der = uno = None
        if self.condExcep != None:
            uno = self.condExcep.interpretar(arbol, tablaSimbolo)
            if isinstance(uno, Error):
                return uno
            if self.condExcep.tipo == TipoDato.NOTHING:
                return Error("Error Semantico", "Variable con dato nulo no puede ser ejecutada", self.linea, self.columna)
        else:
            if self.relacion == opLogico.AND:
                self.tipo = TipoDato.BOOLEANO
                izq = self.cond1.interpretar(arbol, tablaSimbolo)
                if isinstance(izq, Error):
                    return izq
                if izq:
                    der = self.cond2.interpretar(arbol, tablaSimbolo)
                    if isinstance(der, Error):
                        return der
                    if der:
                        return True
                    else:
                        return False
                else:
                    return False
            izq = self.cond1.interpretar(arbol, tablaSimbolo)
            if isinstance(izq, Error):
                return izq
            der = self.cond2.interpretar(arbol, tablaSimbolo)
            if isinstance(der, Error):
                return der
            if self.cond1.tipo == TipoDato.NOTHING or self.cond2.tipo == TipoDato.NOTHING:
                return Error("Error Semantico", "Variable con dato nulo no puede ser ejecutada", self.linea, self.columna)
        self.tipo = TipoDato.BOOLEANO

        if self.relacion == opLogico.OR:
            return True if izq or der else False
        elif self.relacion == opLogico.NOT:
            return not uno
