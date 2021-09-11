from controlador.analizador.simbolos.Simbolo import Simbolo
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Asignacion(Instruccion):
    def __init__(self, identificador, valor, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.valor = valor

    def interpretar(self, arbol, tablaSimbolo):
        variable = tablaSimbolo.getVariable(self.identificador)
        if variable != None:
            val = self.valor.interpretar(arbol, tablaSimbolo)
            if variable.tipo != self.valor.tipo:
                return Error("Error Semantico", "Variable {} con tipo de dato diferente".format(self.identificador), self.linea, self.columna)
            else:
                variable.setValor(val)
                # Actualiza tabla

        else:
            val = self.valor.interpretar(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            if tablaSimbolo.setVariable(Simbolo(self.identificador, self.valor.tipo, val)) != 'La variable existe':
                return Error("Error Semantico", "La variable {} Existe actualmente".format(self.identificador), self.linea, self.columna)
