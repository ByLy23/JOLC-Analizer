from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondIf(Instruccion):
    def __init__(self, expresion, instrucIf, listaInstruccionesElseIf, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.expresion = expresion
        self.condIf = instrucIf
        self.listaInstruccionesElseIf = listaInstruccionesElseIf

    def getNodo(self):
        nodo = NodoAST('CONDICION IF')
        nodo.agregar('if')
        nodo.agregarAST(self.expresion.getNodo())
        for instIf in self.condIf:
            nodo.agregarAST(instIf.getNodo())
        for itm in self.listaInstruccionesElseIf:
            if itm["expresion"] != None:
                nodo.agregar('elseif')
                nodo.agregarAST(itm["expresion"].getNodo())
                for i in itm["instrucciones"]:
                    nodo.agregarAST(i.getNodo())
            else:
                nodo.agregar('else')
                for i in itm["instrucciones"]:
                    nodo.agregarAST(i.getNodo())
        nodo.agregar('end')
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        val = self.expresion.interpretar(arbol, tablaSimbolo)
        if self.expresion.tipo != TipoDato.BOOLEANO:
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
            for item in self.listaInstruccionesElseIf:
                if item["expresion"] != None:
                    val = item["expresion"].interpretar(arbol, tablaSimbolo)
                    if item["expresion"].tipo != TipoDato.BOOLEANO:
                        return Error("Error Semantico", "Dato debe de ser booleano", self.linea, self.columna)
                    if val:
                        nuevaTabla = TablaSimbolos(tablaSimbolo)
                        nuevaTabla.setNombre('Elseif')
                        for i in range(0, len(item["instrucciones"])):
                            a = item["instrucciones"][i].interpretar(
                                arbol, nuevaTabla)
                            # print(item["instrucciones"][i])
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

                        return None
                else:
                    nuevaTabla = TablaSimbolos(tablaSimbolo)
                    nuevaTabla.setNombre('Else')
                    for i in range(0, len(item["instrucciones"])):
                        a = item["instrucciones"][i].interpretar(
                            arbol, nuevaTabla)
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
