from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Simbolo import Simbolo
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Declaracion(Instruccion):
    def __init__(self, tipo, linea, columna, identificador, valor=None):
        super().__init__(tipo, linea, columna)
        self.identificador = identificador
        self.valor = valor

    def interpretar(self, arbol, tablaSimbolo):
        if self.valor == None:  # valor Nothing
            if tablaSimbolo.setVariable(Simbolo(self.identificador, self.tipo, None)) == 'La variable existe':
                return Error("Error Semantico", "La variable {} Existe actualmente".format(self.identificador), self.linea, self.columna)
            # else: nuevoSimbolo y tabla y todo eso
        else:
            if tablaSimbolo.setVariable(Simbolo(self.identificador, self.tipo, None)) == 'La variable existe':
                return Error("Error Semantico", "La variable {} Existe actualmente".format(self.identificador), self.linea, self.columna)
            # else:
                # Actualiza tabla y eso
