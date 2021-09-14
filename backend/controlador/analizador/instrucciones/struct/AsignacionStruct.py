from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class AsignacionStruct(Instruccion):
    def __init__(self, identificador, parametro, expresion, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.parametro = parametro
        self.expresion = expresion

    def interpretar(self, arbol, tablaSimbolo):
        variable = tablaSimbolo.getVariable(self.identificador)
        if variable == None:
            return Error("Error Semantico", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
        valStruct = arbol.getStruct(variable.tipoStruct)
        # print(variable.getIdentificador())
        # print(valStruct)
        # print(variable.tipoStruct)
        if valStruct == None:
            return Error("Error Semantico", "La variable no es estruct", self.linea, self.columna)
        if not valStruct.mutable:
            return Error("Error Semantico", "El struct no es de tipo mutable", self.linea, self.columna)
        for param in variable.getValor():
            if param.getIdentificador() == self.parametro:
                self.tipo = param.getTipo()
                val = self.expresion.interpretar(arbol, tablaSimbolo)
                # print(self.expresion.tipo)
                if isinstance(val, Error):
                    return val
                if self.noNulo(valStruct, self.parametro):
                    if param.getTipo() != self.expresion.tipo:
                        return Error("Error Semantico", "tipo de dato diferente", self.linea, self.columna)
                param.setTipo(self.expresion.tipo)
                param.setValor(val)
                return None
        return Error("Error Semantico", "No existe este parametro dentro del struct", self.linea, self.columna)

    def noNulo(self, struct, parametro):
        for param in struct.parametros:
            if param["identificador"] == parametro:
                if param["tipato"] == None:
                    return False
                return True
