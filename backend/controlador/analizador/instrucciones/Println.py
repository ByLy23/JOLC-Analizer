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
        if self.expresion.tipo == TipoDato.ARREGLO:
            arbol.actualizaConsola(self.impresion(valor)+"\n")

        else:
            arbol.actualizaConsola(str(valor)+"\n")

    def impresion(self, valor):
        dato = ""
        dato = dato+"[ "
        for val in valor.values():
            if val.tipo == TipoDato.ARREGLO:
                dato = dato+self.impresion(val.getValor())+", "
            else:
                dato = dato+str(val.getValor())+", "
        dato = dato+"]"
        return dato
