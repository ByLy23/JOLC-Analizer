from ..abstracto.Instruccion import Instruccion
from ..excepciones.Error import Error
from ..simbolos.Arbol import Arbol


class Println(Instruccion):
    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna

    def interpretar(self, arbol, tablaSimbolo):
        valor = self.expresion.interpretar(arbol, tablaSimbolo)
        if isinstance(valor, Error):
            return valor
        arbol.getConsola(valor+"\n")
