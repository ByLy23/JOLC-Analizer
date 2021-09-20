from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class AccesoStruct(Instruccion):
    def __init__(self, identificador, parametro, accesos, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.parametro = parametro
        self.accesos = accesos

    def getNodo(self):
        nodo = NodoAST('ACCESO STRUCT')
        nodo.agregar(self.identificador.getNodo())
        nodo.agregar('.')
        nodo.agregar(self.parametro)
        if self.accesos != None:
            for acceso in self.accesos:
                nodo.agregar('[')
                nodo.agregar(acceso.getNodo())
                nodo.agregar(']')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        identificador = self.identificador.interpretar(arbol, tablaSimbolo)
        if isinstance(identificador, Error):
            return identificador
        if self.identificador.tipo != TipoDato.STRUCT:
            return Error("Error Semantico", "Variable no es struct", self.linea, self.columna)

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
                    self.tipo = variable.tipo
                    self.tipoStruct = variable.tipoStruct
                    self.mutable = variable.mutable
                    return variable.getValor()
                else:
                    self.tipo = param.getTipo()
                    self.tipoStruct = param.tipoStruct
                    self.mutable = param.mutable
                    # print(self.tipo)
                    # print(param.getValor())
                    return param.getValor()
        return Error("Error Semantico", "No existe este parametro dentro del struct", self.linea, self.columna)
        # variable = tablaSimbolo.getVariable(self.identificador)
        # self.tipo = variable.tipo
        # self.tipoStruct = variable.tipoStruct
        # self.mutable = variable.mutable
        # # print(variable.getValor()[0].getIdentificador())
        # if variable == None:
        #     return Error("Error Semantico", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
        # # print(self.identificador)
        # # print(variable.getValor())
        # # print(variable.getIdentificador())
        # # print(self.linea, self.columna)
        # for param in variable.getValor():
        #     print(param.getIdentificador(), self.parametro)
        #     if param.getIdentificador() == self.parametro:
        #         # print(param.getIdentificador())
        #         self.tipo = param.getTipo()
        #         # print(self.tipo)
        #         # print(param.getValor())
        #         return param.getValor()
        # return Error("Error Semantico", "No existe este parametro dentro del struct", self.linea, self.columna)
