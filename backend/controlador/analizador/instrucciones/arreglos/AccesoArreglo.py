from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class AccesoArreglo(Instruccion):
    def __init__(self, identificador, listaAccesos, linea, columna):
        super().__init__(TipoDato.ARREGLO, linea, columna)
        self.identificador = identificador
        self.listaAccesos = listaAccesos

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
        self.tipo = variable.tipo
        self.tipoStruct = variable.tipoStruct
        self.mutable = variable.mutable
        return variable.getValor()
