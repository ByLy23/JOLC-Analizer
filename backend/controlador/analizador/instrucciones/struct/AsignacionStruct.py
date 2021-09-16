from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class AsignacionStruct(Instruccion):
    def __init__(self, identificador, parametro, expresion, accesos, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.parametro = parametro
        self.expresion = expresion
        self.accesos = accesos

    def interpretar(self, arbol, tablaSimbolo):

        identificador = self.identificador.interpretar(arbol, tablaSimbolo)
        valStruct = arbol.getStruct(self.identificador.tipoStruct)
        if isinstance(identificador, Error):
            return identificador
        # print(self.identificador.tipo)
        if self.identificador.tipo != TipoDato.STRUCT:
            return Error("Error Semantico", "Variable no es struct", self.linea, self.columna)
        # print(identificador)

        for param in identificador:

            if param.getIdentificador() == self.parametro:
                if self.accesos != None:
                    if param.tipo != TipoDato.ARREGLO:
                        return Error("Error Semantico", "La variable debe ser de tipo arreglo", self.linea, self.columna)
                    variable = param
                    for acceso in self.accesos:
                        val = acceso.interpretar(arbol, tablaSimbolo)
                        if isinstance(val, Error):
                            return val
                        if acceso.tipo != TipoDato.ENTERO:
                            return Error("Error Semantico", "El tipo de dato debe ser entero", self.linea, self.columna)
                        try:
                            variable = variable.getValor()[str(val)]
                        except:
                            return Error("Error Semantico", "No se encontro el acceso", self.linea, self.columna)
                    valor = self.expresion.interpretar(arbol, tablaSimbolo)

                    if isinstance(valor, Error):
                        return valor
                    variable.tipo = self.expresion.tipo
                    variable.tipoStruct = self.expresion.tipoStruct
                    variable.mutable = self.expresion.mutable
                    variable.setValor(valor)
                    return None
                else:
                    self.tipo = param.getTipo()
                    val = self.expresion.interpretar(arbol, tablaSimbolo)
                    # print(self.expresion.tipo)
                    if isinstance(val, Error):
                        return val
                    if self.noNulo(valStruct, self.parametro):
                        if param.getTipo() != self.expresion.tipo:
                            return Error("Error Semantico", "tipo de dato diferente", self.linea, self.columna)
                    param.setTipo(self.expresion.tipo)
                    param.tipoStruct = self.expresion.tipoStruct
                    param.mutable = self.expresion.mutable
                    param.setValor(val)
                    return None
                    # self.tipo = param.getTipo()
                    # self.tipoStruct = param.tipoStruct
                    # self.mutable = param.mutable
                    # # print(self.tipo)
                    # # print(param.getValor())
                    # return param.getValor()
        return Error("Error Semantico", "No existe este parametro dentro del struct", self.linea, self.columna)
        # variable = tablaSimbolo.getVariable(self.identificador)
        # if variable == None:
        #     return Error("Error Semantico", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
        # valStruct = arbol.getStruct(variable.tipoStruct)
        # # print(variable.getIdentificador())
        # # print(valStruct)
        # # print(variable.tipoStruct)
        # if valStruct == None:
        #     return Error("Error Semantico", "La variable no es estruct", self.linea, self.columna)
        # if not valStruct.mutable:
        #     return Error("Error Semantico", "El struct no es de tipo mutable", self.linea, self.columna)
        # for param in variable.getValor():
        #     if param.getIdentificador() == self.parametro:
        #         self.tipo = param.getTipo()
        #         val = self.expresion.interpretar(arbol, tablaSimbolo)
        #         # print(self.expresion.tipo)
        #         if isinstance(val, Error):
        #             return val
        #         if self.noNulo(valStruct, self.parametro):
        #             if param.getTipo() != self.expresion.tipo:
        #                 return Error("Error Semantico", "tipo de dato diferente", self.linea, self.columna)
        #         param.setTipo(self.expresion.tipo)
        #         param.setValor(val)
        #         return None
        # return Error("Error Semantico", "No existe este parametro dentro del struct", self.linea, self.columna)

    def noNulo(self, struct, parametro):
        if struct != None:
            for param in struct.parametros:
                if param["identificador"] == parametro:
                    if param["tipato"] == None:
                        return False
                    return True
        else:
            return False
