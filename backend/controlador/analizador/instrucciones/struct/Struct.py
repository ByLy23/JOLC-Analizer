from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Struct(Instruccion):
    def __init__(self, mutable, identificador, parametros, linea, columna):
        super().__init__(TipoDato.STRUCT, linea, columna)
        self.mutable = mutable
        self.identificador = identificador
        self.parametros = parametros

    def interpretar(self, arbol, tablaSimbolo):
        arbol.getStructs().append(self)
