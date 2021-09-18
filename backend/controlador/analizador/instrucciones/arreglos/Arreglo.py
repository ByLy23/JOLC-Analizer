from controlador.analizador.simbolos.Simbolo import Simbolo
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Arreglo(Instruccion):
    def __init__(self, expresiones, linea, columna):
        super().__init__(TipoDato.ARREGLO, linea, columna)
        self.expresiones = expresiones

    def interpretar(self, arbol, tablaSimbolo):
        iterador = 1
        valorArreglo = {}
        for expresion in self.expresiones:
            val = expresion.interpretar(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            simbolo = Simbolo(str(iterador), expresion.tipo, val)
            simbolo.tipoStruct = expresion.tipoStruct
            simbolo.mutable = expresion.mutable
            valorArreglo[str(iterador)] = simbolo
            iterador = iterador+1
        self.mutable = True

        return valorArreglo
