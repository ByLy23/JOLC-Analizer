from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion
from math import *


class FuncNativa(Instruccion):
    def __init__(self, nombre, argumentos, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.nombre = nombre
        self.argumentos = argumentos

    def interpretar(self, arbol, tablaSimbolo):
        exp = self.nombre
        if isinstance(exp, Error):
            return exp
        if self.argumentos["exp2"] != None:
            arg1 = self.argumentos["exp1"].interpretar(arbol, tablaSimbolo)
            if isinstance(arg1, Error):
                return arg1
            arg2 = self.argumentos["exp2"].interpretar(arbol, tablaSimbolo)
            if isinstance(arg2, Error):
                return arg2
            # print(exp, arg1, arg2)
        else:
            arg1 = self.argumentos["exp1"].interpretar(arbol, tablaSimbolo)
            if isinstance(arg1, Error):
                return arg1
            if exp == "typeof":  # ARGUMENTO
                self.tipo = TipoDato.CADENA
                return str(self.argumentos["exp1"].tipo)[9:]
            elif exp == "float":  # ARGUMENTO
                if self.argumentos["exp1"].tipo == TipoDato.ENTERO:
                    self.tipo = TipoDato.DECIMAL
                    return float(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser entero", self.linea, self.columna)
            elif exp == "trunc":  # ARGUMENTO
                if self.argumentos["exp1"].tipo == TipoDato.DECIMAL:
                    self.tipo = TipoDato.ENTERO
                    return trunc(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser decimal", self.linea, self.columna)
            elif exp == "string":  # ARGUMENTO
                self.tipo = TipoDato.CADENA
                return str(arg1)
            elif exp == "sqrt":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return sqrt(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
            elif exp == "log10":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return log10(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
            elif exp == "sin":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return sin(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
            elif exp == "cos":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return cos(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
            elif exp == "tan":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return tan(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
