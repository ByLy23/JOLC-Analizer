from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Identificador(Instruccion):
    def __init__(self, identificador, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador

    def interpretar(self, arbol, tablaSimbolo):
        variable = tablaSimbolo.getVariable(self.identificador)
        if variable == None:
            return Error("Error Semantico", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
        self.tipo = variable.tipo
        return variable.getValor()
