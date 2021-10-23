from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.excepciones.Error import Error
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

    def traducir(self, arbol, tablaSimbolo):
        if self.eSalida() != None:
            return {'temporal': "", 'codigo': arbol.goto(self.eSalida())}
        return Error("Error de Compilacion", "Sentencia fuera de ciclo", self.linea, self.columna)

    def interpretar(self, arbol, tablaSimbolo):
        return 'ByLy23'
