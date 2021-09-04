from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondDefault(Instruccion):
    def __init__(self, instrucciones, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.instrucciones = instrucciones

    def interpretar(self, arbol, tablaSimbolo):
        nuevaTabla = TablaSimbolos(tablaSimbolo)
        for i in range(0, len(self.instrucciones)):
            a = self.instrucciones[i].interpretar(arbol, nuevaTabla)
            if isinstance(a, Error):
                arbol.getErrores().append(a)
                arbol.actualizaConsola(a.retornaError())
            # if return, continue, break
