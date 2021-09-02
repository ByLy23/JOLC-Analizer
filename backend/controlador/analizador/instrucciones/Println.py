from ..abstracto.Instruccion import Instruccion
from ..excepciones.Error import Error
from ..simbolos.Arbol import Arbol
from ..simbolos.Tipo import TipoDato


class Println(Instruccion):
    def __init__(self, linea, columna, expresion=""):
        super().__init__(TipoDato.CADENA, linea, columna)
        self.expresion = expresion
        self.linea = linea
        self.columna = columna

    def interpretar(self, arbol, tablaSimbolo):
        valor = self.expresion.interpretar(arbol, tablaSimbolo)
        if isinstance(valor, Error):
            return valor
        arbol.actualizaConsola(str(valor)+"\n")
