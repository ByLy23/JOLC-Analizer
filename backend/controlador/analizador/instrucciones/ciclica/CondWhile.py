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
        while True:
            cond = self.condicion.interpretar(arbol, tablaSimbolo)
            if isinstance(cond, Error):
                return cond
            if self.condicion.tipo == TipoDato.BOOLEANO:
                if bool(cond) == True:
                    nuevaTabla = TablaSimbolos(tablaSimbolo)
                    nuevaTabla.setNombre('While')
                    for i in self.expresion:
                        a = i.interpretar(arbol, nuevaTabla)
                        if isinstance(a, Error):
                            arbol.getErrores().append(a)
                            arbol.actualizaConsola(a.retornaError())
                        if isinstance(a, Return):
                            return a
                        if a == 'ByLyContinue':
                            break
                        if a == 'ByLy23':
                            return
                else:
                    break
