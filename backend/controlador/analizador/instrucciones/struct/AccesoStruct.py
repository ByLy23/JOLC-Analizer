from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class AccesoStruct(Instruccion):
    def __init__(self, identificador, parametro, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.parametro = parametro

    def interpretar(self, arbol, tablaSimbolo):
        variable = tablaSimbolo.getVariable(self.identificador)
        if variable == None:
            return Error("Error Semantico", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
        for param in variable.getValor():
            if param.getIdentificador() == self.parametro:
                self.tipo = param.getTipo()
                return param.getValor()
        return Error("Error Semantico", "No existe este parametro dentro del struct", self.linea, self.columna)
