from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondSwitch(Instruccion):
    def __init__(self, expresion, listaCasos, defecto, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.expresion = expresion
        self.listaCasos = listaCasos
        self.defecto = defecto

    def interpretar(self, arbol, tablaSimbolo):
        if self.listaCasos != None:
            for caso in self.listaCasos:
                caso.expresionCase = self.expresion
                a = caso.interpretar(arbol, tablaSimbolo)
                if isinstance(a, Error):
                    arbol.getErrores().append(a)
                    arbol.actualizaConsola(a.retornaError())
                # if return, continue,break
        if self.defecto != None:
            a = self.defecto.interpretar(arbol, tablaSimbolo)
            if isinstance(a, Error):
                arbol.getErrores().append(a)
                arbol.actualizaConsola(a.retornaError())
            # if return, continue, break
