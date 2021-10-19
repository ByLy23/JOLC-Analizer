from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.TablaSimbolosC3D import TablaSimbolosC3D
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondWhile(Instruccion):
    def __init__(self, condicion, expresion, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.condicion = condicion
        self.expresion = expresion

    def getNodo(self):
        nodo = NodoAST('CONDICION WHILE')
        nodo.agregar('while')
        nodo.agregarAST(self.condicion.getNodo())
        for exp in self.expresion:
            nodo.agregarAST(exp.getNodo())
        nodo.agregar('end')
        nodo.agregar(';')
        return nodo

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        lControl = arbol.newLabel()
        lVerdadero = arbol.newLabel()
        lFalso = arbol.newLabel()
        codigo += arbol.getLabel(lControl)
        cond = self.condicion.traducir(arbol, tablaSimbolo)
        if isinstance(cond, Error):
            return cond
        codigo += arbol.masStackV(tablaSimbolo.tamanio)
        if self.condicion.tipo == TipoDato.BOOLEANO:
            codigo += cond["codigo"]
            codigo += arbol.getCond2(cond["temporal"], "==", "1.0", lVerdadero)
            codigo += arbol.goto(lFalso)
            codigo += arbol.getLabel(lVerdadero)
            nuevaTabla = TablaSimbolosC3D(tablaSimbolo)
            nuevaTabla.setNombre('While')
            aux = ""
            for i in self.expresion:
                i.eSetSalida(lFalso)
                i.eSetContinua(lControl)
                a = i.traducir(arbol, nuevaTabla)
                aux += a["codigo"]
                if isinstance(a, Error):
                    arbol.getErrores().append(a)
                    arbol.actualizaConsola(a.retornaError())
            codigo += aux
            codigo += arbol.goto(lControl)
            codigo += arbol.getLabel(lFalso)
        '''
        LC:
        if a>b goto LV
        goto LF
        LV: 
        instrucciones
        goto LC
        LF:
        '''
        codigo += arbol.menosStackV(tablaSimbolo.tamanio)
        return {'temporal': "", 'codigo': codigo}

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
