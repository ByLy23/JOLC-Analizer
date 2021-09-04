from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondIf(Instruccion):
    def __init__(self, cond1, condIf, condElse, condElseIf, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.cond1 = cond1
        self.condIf = condIf
        self.condElse = condElse
        self.condElseIf = condElseIf

    def interpretar(self, arbol, tablaSimbolo):
        val = self.cond1.interpretar(arbol, tablaSimbolo)
        if self.cond1.tipo != TipoDato.BOOLEANO:
            return Error("Error Semantico", "Dato debe de ser booleano", self.linea, self.columna)
        if val:
            nuevaTabla = TablaSimbolos(tablaSimbolo)
            nuevaTabla.setNombre('If')
            for i in range(0, len(self.condIf)):
                a = self.condIf[i].interpretar(arbol, nuevaTabla)
                if isinstance(a, Error):
                    arbol.getErrores().append(a)
                    arbol.actualizaConsola(a.retornaError())
                # If return, continue y break
                if isinstance(a, Return):
                    return a
                if a == 'ByLyContinue':
                    return a
                if a == 'ByLy23':
                    return a
        else:
            if self.condElse != None:
                nuevaTabla = TablaSimbolos(tablaSimbolo)
                nuevaTabla.setNombre('else')
                for i in range(0, len(self.condElse)):
                    a = self.condElse[i].interpretar(arbol, nuevaTabla)
                    if isinstance(a, Error):
                        arbol.getErrores().append(a)
                        arbol.actualizaConsola(a.retornaError())
                    # If return, continue y break
                    if isinstance(a, Return):
                        return a
                    if a == 'ByLyContinue':
                        return a
                    if a == 'ByLy23':
                        return a
            elif self.condElseIf != None:
                b = self.condElseIf.interpretar(arbol, tablaSimbolo)
                if isinstance(b, Error):
                    return b
                # If return,continue,break
                if isinstance(b, Return):
                    return b
                if b == 'ByLyContinue':
                    return b
                if b == 'ByLy23':
                    return b
