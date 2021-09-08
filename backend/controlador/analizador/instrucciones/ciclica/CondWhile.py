from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondWhile(Instruccion):
    def __init__(self, condicion, expresion, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.condicion = condicion
        self.expresion = expresion

    def interpretar(self, arbol, tablaSimbolo):
        val = self.condicion.interpretar(arbol, tablaSimbolo)
        if isinstance(val, Error):
            return val
        if self.condicion.tipo != TipoDato.BOOLEANO:
            return Error("Error Semantico", "Dato debe de ser booleano", self.linea, self.columna)
        while self.condicion.interpretar(arbol, tablaSimbolo):
            nuevaTabla = TablaSimbolos(tablaSimbolo)
            nuevaTabla.setNombre('While')
            for i in range(0, len(self.expresion)):
                a = self.expresion[i].interpretar(arbol, nuevaTabla)
                if isinstance(a, Error):
                    arbol.getErrores().append(a)
                    arbol.actualizaConsola(a.retornaError())
                if isinstance(a, Return):
                    return a
                if a == 'ByLyContinue':
                    break
                if a == 'ByLy23':
                    return
