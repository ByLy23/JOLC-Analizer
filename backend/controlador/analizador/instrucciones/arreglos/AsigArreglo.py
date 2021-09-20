from math import exp
from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class AsigArreglo(Instruccion):
    def __init__(self, identificador, listaAccesos, expresion, linea, columna):
        super().__init__(TipoDato.ARREGLO, linea, columna)
        self.identificador = identificador
        self.listaAccesos = listaAccesos
        self.expresion = expresion

    def getNodo(self):
        nodo = NodoAST('ASIGNACION ARREGLO')
        nodo.agregar(self.identificador)
        for acceso in self.listaAccesos:
            nodo.agregar('[')
            nodo.agregarAST(acceso.getNodo())
            nodo.agregar(']')
        nodo.agregar('=')
        nodo.agregarAST(self.expresion.getNodo())
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        variable = tablaSimbolo.getVariable(self.identificador)
        if variable == None:
            return Error("Error Semantico", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
        if variable.tipo != TipoDato.ARREGLO:
            return Error("Error Semantico", "La variable debe ser de tipo arreglo", self.linea, self.columna)
        for acceso in self.listaAccesos:
            val = acceso.interpretar(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            if acceso.tipo != TipoDato.ENTERO:
                return Error("Error Semantico", "El tipo de dato debe ser entero", self.linea, self.columna)
            try:
                variable = variable.getValor()[str(val)]
            except:
                return Error("Error Semantico", "No se encontro el acceso", self.linea, self.columna)
        exp = self.expresion.interpretar(arbol, tablaSimbolo)
        if isinstance(exp, Error):
            return exp
        variable.tipo = self.expresion.tipo
        variable.tipoStruct = self.expresion.tipoStruct
        variable.mutable = self.expresion.mutable
        variable.setValor(exp)
