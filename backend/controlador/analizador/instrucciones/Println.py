from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.instrucciones.struct.AccesoStruct import AccesoStruct
from ..abstracto.Instruccion import Instruccion
from ..excepciones.Error import Error
from ..simbolos.Arbol import Arbol
from ..simbolos.Tipo import TipoDato


class Println(Instruccion):
    def __init__(self, linea, columna, expresion=""):
        super().__init__(TipoDato.CADENA, linea, columna)
        self.expresion = expresion
        self.linea = linea
        self.columna = columna

    def getNodo(self):
        nodo = NodoAST('PRINTLN')
        nodo.agregar('println')
        nodo.agregar('(')
        for exp in self.expresion:
            nodo.agregarAST(exp.getNodo())
        nodo.agregar(')')
        nodo.agregar(';')
        return nodo

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        for valor in self.expresion:
            variable = valor.traducir(arbol, tablaSimbolo)
            if isinstance(variable, Error):
                return variable
            if variable == None:
                err = Error(
                    "Error Semantico", "No existe ningun valor que mostrar", self.linea, self.columna)
                arbol.getErrores().append(err)
                arbol.actualizaConsola(err.retornaError())
            codigo += variable["codigo"]
            # se imprime segun el tipo
            if valor.tipo == TipoDato.ENTERO:

                codigo += arbol.imprimir(
                    '"%d", int({})'.format(variable["temporal"]))
                #fmt.Printf("%d", int(expresion))
            elif valor.tipo == TipoDato.DECIMAL:
                codigo += arbol.imprimir(
                    '"%f", {}'.format(variable["temporal"]))
                # fmt.Printf("%f", 32.2)
            elif valor.tipo == TipoDato.CARACTER:
                codigo += arbol.imprimir(
                    '"%c", {}'.format(variable["temporal"]))
                # fmt.Printf("%c", 36)
            elif valor.tipo == TipoDato.BOOLEANO:
                temp = arbol.newTemp()
                lTrue = arbol.newLabel()
                lFalse = arbol.newLabel()
                lSalida = arbol.newLabel()
                codigo += arbol.assigTemp1(temp["temporal"],
                                           variable["temporal"])
                codigo += arbol.getCond2(temp["temporal"],
                                         " == ", "1.0", lTrue)
                codigo += arbol.goto(lFalse)
                codigo += arbol.getLabel(lTrue)
                codigo += arbol.imprimir('"%c", 116')  # t
                codigo += arbol.imprimir('"%c", 114')  # r
                codigo += arbol.imprimir('"%c", 117')  # u
                codigo += arbol.imprimir('"%c", 101')  # e
                codigo += arbol.goto(lSalida)
                codigo += arbol.getLabel(lFalse)
                codigo += arbol.imprimir('"%c", 102')  # f
                codigo += arbol.imprimir('"%c", 97')  # a
                codigo += arbol.imprimir('"%c", 108')  # l
                codigo += arbol.imprimir('"%c", 115')  # s
                codigo += arbol.imprimir('"%c", 101')  # e
                codigo += arbol.getLabel(lSalida)
                '''
                t1=temporal
                if(t1==1.0){goto true}
                goto false
                true:
                imprimir(true) caracter por caracter
                goto salida
                false:
                imprimir(false) caracter por caracter
                salida:
                
                '''
            elif valor.tipo == TipoDato.CADENA:
                tempo = arbol.newTemp()
                codigo += variable["codigo"]
                indice = variable["heap"]
                tempL = arbol.newTemp()
                loop = arbol.newLabel()
                lSalida = arbol.newLabel()
                impresion = arbol.newLabel()
                codigo += arbol.assigTemp1(tempo["temporal"], indice)
                codigo += arbol.getHeap(tempL["temporal"], tempo["temporal"])
                codigo += arbol.goto(loop)
                codigo += arbol.getLabel(loop)
                codigo += arbol.getHeap(tempL["temporal"], tempo["temporal"])
                codigo += arbol.getCond2(tempL["temporal"],
                                         "==", "-1.0", lSalida)
                codigo += arbol.getCond2(tempL["temporal"],
                                         "==", "0.0", impresion)
                codigo += arbol.imprimir(
                    '"%c", int({})'.format(tempL["temporal"]))
                codigo += arbol.getLabel(impresion)
                codigo += arbol.assigTemp2(tempo["temporal"],
                                           tempo["temporal"], "+", "1")
                codigo += arbol.goto(loop)
                codigo += arbol.getLabel(lSalida)

        codigo += arbol.imprimir('"\\n"')
        return {'temporal': "", 'codigo': codigo}

    def interpretar(self, arbol, tablaSimbolo):
        for valor in self.expresion:
            variable = valor.interpretar(arbol, tablaSimbolo)
            if isinstance(variable, Error):
                return variable
            if variable == None:
                err = Error(
                    "Error Semantico", "No existe ningun valor que mostrar", self.linea, self.columna)
                arbol.getErrores().append(err)
                arbol.actualizaConsola(err.retornaError()+"\n")
            if valor.tipo == TipoDato.ARREGLO:
                arbol.actualizaConsola(self.impresion(variable).replace(
                    '(,', '("",').replace(',,', ',"",').replace(',)', ',"")'))
            elif valor.tipo == TipoDato.STRUCT:
                if isinstance(valor, AccesoStruct):
                    arbol.actualizaConsola(
                        valor.parametro+self.impresionStruct(variable).replace('(,', '("",').replace(',,', ',"",').replace(',)', ',"")'))
                else:
                    arbol.actualizaConsola(
                        valor.identificador+self.impresionStruct(variable).replace('(,', '("",').replace(',,', ',"",').replace(',)', ',"")'))
            else:
                arbol.actualizaConsola(str(variable).replace(
                    '(,', '("",').replace(',,', ',"",').replace(',)', ',"")'))
        arbol.actualizaConsola("\n")

    def impresionStruct(self, valor):
        dato = ""
        dato = dato+"("
        for val in valor:
            if val.tipo == TipoDato.ARREGLO:
                dato = dato+self.impresion(val.getValor())+","
            elif val.tipo == TipoDato.STRUCT:
                dato = dato+val.tipoStruct + \
                    self.impresionStruct(val.getValor())+","
            else:
                dato = dato+str(val.getValor())+","
        dato = dato[:-1]+")"
        return dato

    def impresion(self, valor):
        dato = ""
        dato = dato+"["
        for val in valor.values():
            if val.tipo == TipoDato.ARREGLO:
                dato = dato+self.impresion(val.getValor())+","
            elif val.tipo == TipoDato.STRUCT:
                dato = dato+val.tipoStruct + \
                    self.impresionStruct(val.getValor())+","
            else:
                dato = dato+str(val.getValor())+","
        dato = dato[:-1]+"]"
        return dato
