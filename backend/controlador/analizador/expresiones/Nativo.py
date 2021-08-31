from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Nativo(Instruccion):
    def __init__(self, tipo, valor, linea, columna):
        super().__init__(tipo, linea, columna)
        self.valor = valor

    def interpretar(self, arbol, tablaSimbolo):
        if self.tipo == TipoDato.BOOLEANO:
            return self.valor == 'true'
        return self.valor
