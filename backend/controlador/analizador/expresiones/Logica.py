from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato, opLogico
from controlador.analizador.abstracto.Instruccion import Instruccion


class Logica(Instruccion):
    def __init__(self, relacion, linea, columna, cond1, cond2=None):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.relacion = relacion
        self.cond1 = cond1
        self.condExcep = None
        if cond2 == None:
            self.condExcep = cond1
        else:
            self.cond1 = cond1
            self.cond2 = cond2

    def getNodo(self):
        nodo = NodoAST('LOGICA')
        if self.condExcep != None:
            nodo.agregar(self.relacion, 'log', self.relacion)
            nodo.agregarAST(self.condExcep.getNodo())
        else:
            nodo.agregarAST(self.cond1.getNodo())
            nodo.agregar(self.relacion, 'log', self.relacion)
            nodo.agregarAST(self.cond2.getNodo())
        return nodo

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        izq = der = uno = None
        if self.condExcep != None:
            uno = self.condExcep.traducir(arbol, tablaSimbolo)
            if isinstance(uno, Error):
                return uno
            if self.condExcep.tipo == TipoDato.NOTHING:
                return Error("Error Semantico", "Variable con dato nulo no puede ser ejecutada", self.linea, self.columna)
        else:
            izq = self.cond1.traducir(arbol, tablaSimbolo)
            if isinstance(izq, Error):
                return izq
            der = self.cond2.traducir(arbol, tablaSimbolo)
            if isinstance(der, Error):
                return der
            if self.relacion == opLogico.AND:
                self.tipo = TipoDato.BOOLEANO
                temp = arbol.newTemp()
                lTrue1 = arbol.newLabel()
                lTrue2 = arbol.newLabel()
                lFalse2 = arbol.newLabel()
                codigo += izq["codigo"]
                codigo += der["codigo"]
                codigo += arbol.getCond2(izq["temporal"], "==", "1.0", lTrue1)
                codigo += arbol.assigTemp1(temp["temporal"], "0.0")
                codigo += arbol.goto(lFalse2)
                codigo += arbol.getLabel(lTrue1)
                codigo += arbol.getCond2(der["temporal"], "==", "1.0", lTrue2)
                codigo += arbol.assigTemp1(temp["temporal"], "0.0")
                codigo += arbol.goto(lFalse2)
                codigo += arbol.getLabel(lTrue2)
                codigo += arbol.assigTemp1(temp["temporal"], "1.0")
                codigo += arbol.getLabel(lFalse2)
                '''
                if(a==1){goto Lv1}
                t=0
                goto Lf2
                Lv1:
                if (c ==1){goto Lv2}
                t=0
                goto Lf2
                lv2:
                t=1
                Lf2:
                '''

            if self.cond1.tipo == TipoDato.NOTHING or self.cond2.tipo == TipoDato.NOTHING:
                return Error("Error Semantico", "Variable con dato nulo no puede ser ejecutada", self.linea, self.columna)
        self.tipo = TipoDato.BOOLEANO
        if self.relacion == opLogico.OR:
            temp = arbol.newTemp()
            lTrue1 = arbol.newLabel()
            lTrue2 = arbol.newLabel()
            lFalse2 = arbol.newLabel()
            codigo += izq["codigo"]
            codigo += der["codigo"]
            codigo += arbol.getCond2(izq["temporal"], "==", "1.0", lTrue2)
            codigo += arbol.assigTemp1(temp["temporal"], "0.0")
            codigo += arbol.goto(lTrue1)
            codigo += arbol.getLabel(lTrue1)
            codigo += arbol.getCond2(der["temporal"], "==", "1.0", lTrue2)
            codigo += arbol.assigTemp1(temp["temporal"], "0.0")
            codigo += arbol.goto(lFalse2)
            codigo += arbol.getLabel(lTrue2)
            codigo += arbol.assigTemp1(temp["temporal"], "1.0")
            codigo += arbol.getLabel(lFalse2)
            '''
                if(a==1){goto Lv2}
                t=0
                goto Lv1
                Lv1:
                if (c ==1){goto Lv2}
                t=0
                goto Lf2
                lv2:
                t=1
                Lf2:
                '''
        elif self.relacion == opLogico.NOT:
            temp = arbol.newTemp()
            lTrue1 = arbol.newLabel()
            lFalse2 = arbol.newLabel()
            codigo += uno["codigo"]
            codigo += arbol.getCond2(uno["temporal"], "==", "1.0", lFalse2)
            codigo += arbol.assigTemp1(temp["temporal"], "1.0")
            codigo += arbol.goto(lTrue1)
            codigo += arbol.getLabel(lFalse2)
            codigo += arbol.assigTemp1(temp["temporal"], "0.0")
            codigo += arbol.getLabel(lTrue1)
            '''
                if(a==1){goto Lf1}
                t=1
                goto Lv1
                Lv1:
                Lf1:
                '''
        return {'temporal': temp["temporal"], 'codigo': codigo}

    def interpretar(self, arbol, tablaSimbolo):
        izq = der = uno = None
        if self.condExcep != None:
            uno = self.condExcep.interpretar(arbol, tablaSimbolo)
            if isinstance(uno, Error):
                return uno
            if self.condExcep.tipo == TipoDato.NOTHING:
                return Error("Error Semantico", "Variable con dato nulo no puede ser ejecutada", self.linea, self.columna)
        else:
            if self.relacion == opLogico.AND:
                self.tipo = TipoDato.BOOLEANO
                izq = self.cond1.interpretar(arbol, tablaSimbolo)
                if isinstance(izq, Error):
                    return izq
                if izq:
                    der = self.cond2.interpretar(arbol, tablaSimbolo)
                    if isinstance(der, Error):
                        return der
                    if der:
                        return True
                    else:
                        return False
                else:
                    return False
            izq = self.cond1.interpretar(arbol, tablaSimbolo)
            if isinstance(izq, Error):
                return izq
            der = self.cond2.interpretar(arbol, tablaSimbolo)
            if isinstance(der, Error):
                return der
            if self.cond1.tipo == TipoDato.NOTHING or self.cond2.tipo == TipoDato.NOTHING:
                return Error("Error Semantico", "Variable con dato nulo no puede ser ejecutada", self.linea, self.columna)
        self.tipo = TipoDato.BOOLEANO

        if self.relacion == opLogico.OR:
            return True if izq or der else False
        elif self.relacion == opLogico.NOT:
            return not uno
