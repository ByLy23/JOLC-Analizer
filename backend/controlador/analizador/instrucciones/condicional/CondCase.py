from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondCase(Instruccion):
    expresionCase = None

    def __init__(self, expresion, instrucciones, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.expresion = expresion
        self.instrucciones = instrucciones

    def interpretar(self, arbol, tablaSimbolo):
        val = self.expresion.interpretar(arbol, tablaSimbolo)
        valExpresion = self.expresionCase.interpretar(arbol, tablaSimbolo)
        if self.expresion.tipo == self.expresionCase.tipo:
            if val == valExpresion:
                nuevaTabla = TablaSimbolos(tablaSimbolo)
                nuevaTabla.setNombre('Case')
                for i in range(0, len(self.instrucciones)):
                    a = self.instrucciones[i].interpretar(arbol, tablaSimbolo)
                    if isinstance(a, Error):
                        arbol.getErrores().append(a)
                        arbol.actualizaConsola(a.retornaError())
                    # if return continue break

        else:
            return Error("Error Semantico", "Variable de tipos de datos diferentes", self.linea, self.columna)
