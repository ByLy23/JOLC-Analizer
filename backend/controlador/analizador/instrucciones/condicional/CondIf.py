from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.TablaSimbolosC3D import TablaSimbolosC3D
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondIf(Instruccion):
    def __init__(self, expresion, instrucIf, listaInstruccionesElseIf, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.expresion = expresion
        self.condIf = instrucIf
        self.listaInstruccionesElseIf = listaInstruccionesElseIf

    def traducir(self, arbol, tablaSimbolo):
        '''
        if (a>b) goto Lv
        goto lF
        Lv:
        instrucciones true
        Lf:
        if(c>d) goto Lv2
        goto Lf
        Lv2:
        instrucciones true instrucciones else if
        Lf
        instrucciones else
        goto Ls
        goto Ls
        Ls
        '''
        codigo = ""
        lFalsa1 = arbol.newLabel()
        lSalida = arbol.newLabel()
        val = self.expresion.traducir(arbol, tablaSimbolo)
        if self.expresion.tipo != TipoDato.BOOLEANO:
            return Error("Error Semantico", "Dato debe de ser booleano", self.linea, self.columna)
        lVerdadera = arbol.newLabel()
        '''
    if (a>b) goto Lv
    goto lF
    Lv:
    instrucciones true
    goto Ls
    Lf:
    instrucciones else
    goto Ls
    goto Ls
    Ls
    '''

        codigo += val["codigo"]
        codigo += arbol.getCond2(val["temporal"], "==", "1.0", lVerdadera)
        codigo += arbol.goto(lFalsa1)
        codigo += arbol.getLabel(lVerdadera)
        nuevaTabla = TablaSimbolosC3D(tablaSimbolo)
        codigo += arbol.masStackV(tablaSimbolo.tamanio)
        aux = ""
        for i in range(0, len(self.condIf)):

            self.condIf[i].eSetSalida(lSalida)
            self.condIf[i].eSetContinua(lSalida)
            a = self.condIf[i].traducir(arbol, nuevaTabla)

            if isinstance(a, Error):
                arbol.getErrores().append(a)
                arbol.actualizaConsola(a.retornaError())
                print(a.retornaError())
                continue
            aux += a["codigo"]
        codigo += aux
        codigo += arbol.goto(lSalida)
        codigo += arbol.getLabel(lFalsa1)
        for item in self.listaInstruccionesElseIf:
            if item["expresion"] != None:
                lNuevoVerdadero = arbol.newLabel()
                lNuevoFalso = arbol.newLabel()
                item["expresion"].eSetSalida(lSalida)
                item["expresion"].eSetContinua(lSalida)
                val = item["expresion"].traducir(arbol, tablaSimbolo)
                codigo += val["codigo"]
                codigo += arbol.getCond2(val["temporal"],
                                         "==", "1.0", lNuevoVerdadero)
                codigo += arbol.goto(lNuevoFalso)
                codigo += arbol.getLabel(lNuevoVerdadero)
                if item["expresion"].tipo != TipoDato.BOOLEANO:
                    return Error("Error Semantico", "Dato debe de ser booleano", self.linea, self.columna)
                nuevaTabla = TablaSimbolosC3D(tablaSimbolo)
                nuevaTabla.setNombre('Elseif')
                aux3 = ""
                for i in range(0, len(item["instrucciones"])):
                    item["instrucciones"][i].eSetSalida(lSalida)
                    item["instrucciones"][i].eSetContinua(lSalida)
                    a = item["instrucciones"][i].traducir(
                        arbol, nuevaTabla)
                    aux3 += a["codigo"]
                    # print(item["instrucciones"][i])
                    if isinstance(a, Error):
                        arbol.getErrores().append(a)
                        arbol.actualizaConsola(a.retornaError())
                codigo += aux3
                codigo += arbol.goto(lSalida)
                codigo += arbol.getLabel(lNuevoFalso)
            else:
                nuevaTabla = TablaSimbolosC3D(tablaSimbolo)
                nuevaTabla.setNombre('Else')
                aux2 = ""
                for i in range(0, len(item["instrucciones"])):
                    item["instrucciones"][i].eSetSalida(lSalida)
                    item["instrucciones"][i].eSetContinua(lSalida)
                    a = item["instrucciones"][i].traducir(
                        arbol, nuevaTabla)
                    aux2 = a["codigo"]
                    if isinstance(a, Error):
                        arbol.getErrores().append(a)
                        arbol.actualizaConsola(a.retornaError())
                    # If return, continue y break
                codigo += aux2
                codigo += arbol.goto(lSalida)
        codigo += arbol.getLabel(lSalida)
        codigo += arbol.menosStackV(tablaSimbolo.tamanio)
        return {'temporal': '', 'codigo': codigo}

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
