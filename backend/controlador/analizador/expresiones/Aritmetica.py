
from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato, opAritmetico
from controlador.analizador.abstracto.Instruccion import Instruccion
import math


class Aritmetica(Instruccion):
    def __init__(self, operador,  linea, columna, op1, op2=None):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.operador = operador
        self.operadorUnico = None
        self.temporal = ""
        self.ope = ""
        if operador == opAritmetico.UMENOS:
            self.operadorUnico = op1
        else:
            self.op1 = op1
            self.op2 = op2
# TRADUCIR

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        temp = arbol.newTemp()
        izq = der = uno = None
        if self.operadorUnico != None:
            self.operadorUnico.eSetTemporal(self.eTemporal())
            uno = self.operadorUnico.traducir(arbol, tablaSimbolo)
            if isinstance(uno, Error):
                return uno
        else:
            self.op1.eSetTemporal(self.eTemporal())
            izq = self.op1.traducir(arbol, tablaSimbolo)
            if isinstance(izq, Error):
                return izq
            self.op2.eSetTemporal(self.eTemporal())
            der = self.op2.traducir(arbol, tablaSimbolo)
            if isinstance(der, Error):
                return der
        if self.operador == opAritmetico.MAS:  # FUNCION MAS
            self.ope = "+"
            retorno = self.operador1SumaC3D(izq["temporal"], der["temporal"])
            codigo += izq["codigo"]
            codigo += der["codigo"]
            codigo += arbol.assigTemp2(temp["temporal"],
                                       retorno["op1"], self.ope, retorno["op2"])
        elif self.operador == opAritmetico.MENOS:  # FUNCION MENOS
            self.ope = "-"
            retorno = self.operador1RestaC3D(izq["temporal"], der["temporal"])
            codigo += izq["codigo"]
            codigo += der["codigo"]
            codigo += arbol.assigTemp2(temp["temporal"],
                                       retorno["op1"], self.ope, retorno["op2"])
        elif self.operador == opAritmetico.POR:  # FUNCION POR
            self.ope = "*"
            if self.op1.tipo == TipoDato.CADENA and self.op2.tipo == TipoDato.CADENA:
                self.tipo = TipoDato.CADENA
                retorno = arbol.concatenaString(izq["heap"], der["heap"])
                codigo += izq["codigo"]
                codigo += der["codigo"]
                codigo += retorno["codigo"]
                return {'heap': retorno["heap"], 'codigo': codigo}
            else:
                retorno = self.operador1MultiC3D(
                    izq["temporal"], der["temporal"])
                codigo += izq["codigo"]
                codigo += der["codigo"]
                codigo += arbol.assigTemp2(temp["temporal"],
                                           retorno["op1"], self.ope, retorno["op2"])
        elif self.operador == opAritmetico.MODULO:  # FUNCION MODULO
            self.ope = "%"
            lTrue = arbol.newLabel()
            lSalida = arbol.newLabel()
            retorno = self.operador1DivisionC3D(
                izq["temporal"], der["temporal"])
            codigo += izq["codigo"]
            codigo += der["codigo"]
            codigo += arbol.getCond2(der["temporal"], " != ", "0", lTrue)
            codigo += arbol.imprimir('"%c", 77')  # M
            codigo += arbol.imprimir('"%c", 97')  # a
            codigo += arbol.imprimir('"%c", 116')  # t
            codigo += arbol.imprimir('"%c", 104')  # h
            codigo += arbol.imprimir('"%c", 69')  # E
            codigo += arbol.imprimir('"%c", 114')  # r
            codigo += arbol.imprimir('"%c", 114')  # r
            codigo += arbol.imprimir('"%c", 111')  # o
            codigo += arbol.imprimir('"%c", 114')  # r
            codigo += arbol.assigTemp1(temp["temporal"], "0")
            codigo += arbol.goto(lSalida)
            codigo += arbol.getLabel(lTrue)
            arbol.setImports("\"math\"")
            codigo += arbol.assigTempMod(temp["temporal"],
                                         retorno["op1"], retorno["op2"])

            codigo += arbol.getLabel(lSalida)
        elif self.operador == opAritmetico.DIVI:
            self.ope = "/"
            lTrue = arbol.newLabel()
            lSalida = arbol.newLabel()
            nuevoDer = arbol.newTemp()
            retorno = self.operador1DivisionC3D(
                izq["temporal"], der["temporal"])
            codigo += izq["codigo"]
            codigo += der["codigo"]
            codigo += arbol.getCond2(der["temporal"], " != ", "0", lTrue)
            codigo += arbol.imprimir('"%c", 77')  # M
            codigo += arbol.imprimir('"%c", 97')  # a
            codigo += arbol.imprimir('"%c", 116')  # t
            codigo += arbol.imprimir('"%c", 104')  # h
            codigo += arbol.imprimir('"%c", 69')  # E
            codigo += arbol.imprimir('"%c", 114')  # r
            codigo += arbol.imprimir('"%c", 114')  # r
            codigo += arbol.imprimir('"%c", 111')  # o
            codigo += arbol.imprimir('"%c", 114')  # r
            codigo += arbol.assigTemp1(temp["temporal"], "0")
            codigo += arbol.goto(lSalida)
            codigo += arbol.getLabel(lTrue)
            codigo += arbol.assigTemp1(nuevoDer["temporal"], retorno["op2"])
            codigo += arbol.assigTemp2(temp["temporal"],
                                       retorno["op1"], self.ope, nuevoDer["temporal"])
            codigo += arbol.getLabel(lSalida)

            '''
            if (t2!=0){goto verdadero};
            print matherror
            t3=0;
            goto salida
            verdadero:
            instruccion
            salida:
            '''
        elif self.operador == opAritmetico.POTENCIA:  # PENDIENTES CON DECIMALES
            self.ope = "*"
            lPotencia = arbol.newLabel()
            lSalida = arbol.newLabel()
            lSigue = arbol.newLabel()
            temp = arbol.newTemp()
            tempT2 = arbol.newTemp()
            retorno = self.operador1PotenciaC3D(
                izq["temporal"], der["temporal"])
            t1 = retorno["op1"]
            t2 = retorno["op2"]
            # codigo += retorno["codigo"]
            # verificar si t2 desde el principio es 0
            # verificar si t2 es 1
            # print(t1, t2, temp)
            codigo += izq["codigo"]
            codigo += der["codigo"]
            codigo += arbol.assigTemp1(tempT2["temporal"], t2)
            codigo += arbol.assigTemp1(temp["temporal"], t1)
            codigo += arbol.getLabel(lPotencia)
            codigo += arbol.getCond2(
                tempT2["temporal"], " <= ", "1.0", lSalida)
            codigo += arbol.goto(lSigue)
            codigo += arbol.getLabel(lSigue)
            codigo += arbol.assigTemp2(temp["temporal"],
                                       temp["temporal"], self.ope, t1)
            codigo += arbol.assigTemp2(tempT2["temporal"],
                                       tempT2["temporal"], " - ", "1")
            codigo += arbol.goto(lPotencia)
            codigo += arbol.getLabel(lSalida)
            '''
                  verificaciones de arriba
            #     L1:
            #     if int(t1)==0 goto salida
            #     goto sigue
            #     sigue:
            #     t2=t2*t2
            #     int(t1)=int(t1)-1
            #     goto L1
            #     salida:
            #     temp=t2
            #     '''

            # self.ope = "*"

            # retorno = self.operador1PotenciaC3D(
            #     izq["temporal"], der["temporal"])
            # rAux = ""

            # if(retorno["op2"] == 0):
            #     codigo += izq["codigo"]
            #     codigo += der["codigo"]
            #     codigo += arbol.assigTemp2(temp["temporal"],
            #                                retorno["op1"], self.ope, "1")
            # elif(retorno["op2"] == 1):
            #     codigo += izq["codigo"]
            #     codigo += der["codigo"]
            #     codigo += arbol.assigTemp2(temp["temporal"],
            #                                retorno["op1"], self.ope, retorno["op2"])
            # elif(retorno["op2"] > 1):  # TODO ARREGLAR ESTO PORQUE LA POTENCIA NO ES ASI EQUIS DE
            #
            #     for ins in range(0, retorno["op2"]):
            #         aux = arbol.newTemp()
            #         if ins == 0:
            #             codigo += izq["codigo"]
            #             codigo += der["codigo"]
            #             codigo += arbol.assigTemp2(aux["temporal"],
            #                                        retorno["op1"], self.ope, retorno["op1"])
            #             aux1 = aux["temporal"]
            #             rAux = aux["temporal"]
            #         else:
            #             codigo += izq["codigo"]
            #             codigo += der["codigo"]
            #             codigo += arbol.assigTemp2(aux["temporal"],
            #                                        aux1, self.ope, retorno["op1"])
            #             aux1 = aux["temporal"]
            #             rAux = aux["temporal"]

            #     codigo += izq["codigo"]
            #     codigo += der["codigo"]
            #     codigo += arbol.assigTemp1(temp["temporal"], rAux)

        elif self.operador == opAritmetico.UMENOS:
            self.ope = "-"
            retorno = self.opMenosUnarioC3D(uno["temporal"])
            codigo += uno["codigo"]
            codigo += arbol.assigTemp1(temp["temporal"],
                                       self.ope+uno["temporal"])
        return {'temporal': temp["temporal"], 'codigo': codigo}
    # --------------------SUMAC3D--------------------------

    def operador1SumaC3D(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2SumaC3D(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2SumaC3D(2, op2, izq, der)

    def op2SumaC3D(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}

    # -----------RESTAC3D---------------
    def operador1RestaC3D(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2RestaC3D(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2RestaC3D(2, op2, izq, der)

    def op2RestaC3D(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}

        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
    # ----------------------MULTIPLICACIONC3D--------------------------

    def operador1MultiC3D(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2MultiC3D(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2MultiC3D(2, op2, izq, der)
        elif self.op1.tipo == TipoDato.CADENA:
            return self.op2MultiC3D(4, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2MultiC3D(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 4:
            if op2 == TipoDato.CADENA:
                self.tipo = TipoDato.CADENA
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
    # ------------------- MOD C3D -------------------------

    def operador1ModC3D(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2ModC3D(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2ModC3D(2, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2ModC3D(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)

    # ------------------------------ DIVISION C3D -------------------------------------------
    def operador1DivisionC3D(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2DivisionC3D(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2DivisionC3D(2, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2DivisionC3D(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
    # ------------------- POTENCIAC3D ----------------------------------

    def operador1PotenciaC3D(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2PotenciaC3D(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2PotenciaC3D(2, op2, izq, der)
        elif self.op1.tipo == TipoDato.CADENA:  # TODO
            return self.op2Potencia(4, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2PotenciaC3D(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return {'op1': izq, 'op2': der}
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        # elif numero == 4:
        #     if op2 == TipoDato.ENTERO:
        #         self.tipo = TipoDato.CADENA
        #         cadena = ""
        #         for i in range(0, int(der)):
        #             cadena = cadena+str(izq)
        #         return cadena
        #     else:
        #         return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
     # ----------------------------MENOS UNARIO-------------------------

    def opMenosUnarioC3D(self, izq):
        if self.operadorUnico.tipo == TipoDato.ENTERO:
            self.tipo = TipoDato.ENTERO
            return {'op1': izq}
        elif self.operadorUnico.tipo == TipoDato.DECIMAL:
            self.tipo = TipoDato.DECIMAL
            return {'op1': izq}
    #-----------------------------------------------------------------------------------------------------------------#

    def getNodo(self):
        nodo = NodoAST('ARITMETICA')
        if self.operadorUnico != None:
            nodo.agregar(self.operador, 'ar', self.operador)
            nodo.agregarAST(self.operadorUnico.getNodo())
        else:
            nodo.agregarAST(self.op1.getNodo())
            nodo.agregar(self.operador, 'ar', self.operador)
            nodo.agregarAST(self.op2.getNodo())
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        izq = der = uno = None
        if self.operadorUnico != None:
            uno = self.operadorUnico.interpretar(arbol, tablaSimbolo)
            if isinstance(uno, Error):
                return uno
            if self.operadorUnico.tipo == TipoDato.NOTHING:
                return Error("Error Semantico", "Variable con dato nulo no puede ser ejecutada", self.linea, self.columna)
        else:
            izq = self.op1.interpretar(arbol, tablaSimbolo)
            if isinstance(izq, Error):
                return izq
            der = self.op2.interpretar(arbol, tablaSimbolo)
            if isinstance(der, Error):
                return der
            if self.op1.tipo == TipoDato.NOTHING or self.op2.tipo == TipoDato.NOTHING:
                return Error("Error Semantico", "Variable con dato nulo no puede ser ejecutada", self.linea, self.columna)
        if self.operador == opAritmetico.MAS:
            return self.operador1Suma(izq, der)
        elif self.operador == opAritmetico.MENOS:
            return self.operador1Resta(izq, der)
        elif self.operador == opAritmetico.POR:
            return self.operador1Multi(izq, der)
        elif self.operador == opAritmetico.DIVI:
            return self.operador1Division(izq, der) if (der != 0) or (der != 'false') else Error("Error Sintactico", "No se puede dividir sobre 0", self.linea, self.columna)
        elif self.operador == opAritmetico.POTENCIA:  # PENDIENTES CON DECIMALES
            return self.operador1Potencia(izq, der)
        elif self.operador == opAritmetico.MODULO:  # PENDIENTES CON DECIMALES
            return self.operador1Mod(izq, der)if (der != 0) or (der != 'false') else Error("Error Sintactico", "Error de division", self.linea, self.columna)
        elif self.operador == opAritmetico.UMENOS:
            return self.opMenosUnario(uno)
        else:
            return Error('Error Semantico', 'Operador Invalido', self.linea, self.columna)

    # ----------------------------MENOS UNARIO-------------------------
    def opMenosUnario(self, izq):
        if self.operadorUnico == None:
            return Error('Error Semantico', 'Expresion invalida', self.linea, self.columna)
        if self.operadorUnico.tipo == TipoDato.ENTERO:
            self.tipo = TipoDato.ENTERO
            return int(izq)*-1
        elif self.operadorUnico.tipo == TipoDato.DECIMAL:
            self.tipo = TipoDato.DECIMAL
            return float(izq)*-1.0
        elif self.operadorUnico.tipo == TipoDato.BOOLEANO:
            self.tipo = TipoDato.ENTERO
            return -1 if str(izq).lower() == 'true' else 0

    # -------------------------- SUMA -----------------------------------

    def operador1Suma(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2Suma(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2Suma(2, op2, izq, der)
        elif self.op1.tipo == TipoDato.BOOLEANO:
            return self.op2Suma(3, op2, izq, der)
        elif self.op1.tipo == TipoDato.CARACTER:
            return self.op2Suma(4, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2Suma(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return izq + der
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq)+float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                return int(izq)+1 if str(der).lower() == 'true' else int(izq)
            elif op2 == TipoDato.CARACTER:
                self.tipo = TipoDato.CARACTER
                return chr(int(izq)+ord(str(der)))
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return float(izq) + float(der)
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq)+float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.DECIMAL
                return float(izq)+1 if str(der).lower() == 'true' else float(izq)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 3:
            nuevoIzq = 1 if str(izq).lower() == 'true' else 0
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return nuevoIzq + der
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(nuevoIzq)+float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                return nuevoIzq+1 if str(der).lower() == 'true' else nuevoIzq
            elif op2 == TipoDato.CARACTER:
                self.tipo = TipoDato.CARACTER
                return chr(nuevoIzq+ord(str(der)))
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 4:
            nuevoIzq = ord(str(izq))
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.CARACTER
                return chr(nuevoIzq + der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.CARACTER
                return chr(nuevoIzq+1 if str(der).lower() == 'true' else nuevoIzq)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)

    # ------------------------ RESTA ------------------------

    def operador1Resta(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2Resta(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2Resta(2, op2, izq, der)
        elif self.op1.tipo == TipoDato.BOOLEANO:
            return self.op2Resta(3, op2, izq, der)
        elif self.op1.tipo == TipoDato.CARACTER:
            return self.op2Resta(4, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2Resta(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return int(izq) - int(der)
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq)-float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                return int(izq)-1 if str(der).lower() == 'true' else int(izq)
            # probable borrar
            # elif op2 == TipoDato.CARACTER:
            #     self.tipo = TipoDato.CARACTER
            #     return chr(int(izq)-ord(str(der)))
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return float(izq) - float(der)
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq)-float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.DECIMAL
                return float(izq)-1 if str(der).lower() == 'true' else float(izq)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 3:
            nuevoIzq = 1 if str(izq).lower() == 'true' else 0
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return nuevoIzq - der
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(nuevoIzq)-float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                return nuevoIzq-1 if str(der).lower() == 'true' else nuevoIzq
            elif op2 == TipoDato.CARACTER:
                self.tipo = TipoDato.CARACTER
                return chr(nuevoIzq+ord(str(der)))
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)

     # ------------------------ MULTIPLICACION ------------------------

    def operador1Multi(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2Multi(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2Multi(2, op2, izq, der)
        elif self.op1.tipo == TipoDato.BOOLEANO:
            return self.op2Multi(3, op2, izq, der)
        elif self.op1.tipo == TipoDato.CADENA:
            return self.op2Multi(4, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2Multi(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return izq * der
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq)*float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                return int(izq)*1 if str(der).lower() == 'true' else int(izq)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return float(izq) * float(der)
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq)*float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.DECIMAL
                return float(izq)*1 if str(der).lower() == 'true' else float(izq)*0
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 3:
            nuevoIzq = 1 if str(izq).lower() == 'true' else 0
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return nuevoIzq * der
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(nuevoIzq)*float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                return nuevoIzq*1 if str(der).lower() == 'true' else nuevoIzq*0
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 4:
            if op2 == TipoDato.CADENA:
                self.tipo = TipoDato.CADENA
                return "{}{}".format(izq, der)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
    # -------------------------- DIVISION -----------------------------------

    def operador1Division(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2Division(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2Division(2, op2, izq, der)
        elif self.op1.tipo == TipoDato.BOOLEANO:
            return self.op2Division(3, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2Division(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return float(izq) / float(der)
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq)/float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.DECIMAL
                if str(der).lower() == 'true':
                    return float(izq)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return float(izq) / float(der)
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq)/float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.DECIMAL
                if str(der).lower() == 'true':
                    return float(izq)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 3:
            nuevoIzq = 1 if str(izq).lower() == 'true' else 0
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return float(nuevoIzq) / float(der)
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(nuevoIzq)/float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.DECIMAL
                if str(der).lower() == 'true':
                    return float(nuevoIzq)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)

     # -------------------------- POTENCIA -----------------------------------

    def operador1Potencia(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2Potencia(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2Potencia(2, op2, izq, der)
        elif self.op1.tipo == TipoDato.BOOLEANO:
            return self.op2Potencia(3, op2, izq, der)
        elif self.op1.tipo == TipoDato.CADENA:
            return self.op2Potencia(4, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2Potencia(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return math.pow(int(izq), int(der))
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return math.pow(float(izq), float(der))
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                return math.pow(int(izq), 1) if str(der).lower() == 'true' else math.pow(int(izq), 0)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return math.pow(float(izq), float(der))
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return math.pow(float(izq), float(der))
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.DECIMAL
                return math.pow(float(izq), 1) if str(der).lower() == 'true' else math.pow(float(izq), 0)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 3:
            nuevoIzq = 1 if str(izq).lower() == 'true' else 0
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return math.pow(nuevoIzq, int(der))
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return math.pow(float(nuevoIzq), float(der))
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                return math.pow(nuevoIzq, 1) if str(der).lower() == 'true' else math.pow(nuevoIzq, 0)
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 4:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.CADENA
                cadena = ""
                for i in range(0, int(der)):
                    cadena = cadena+str(izq)
                return cadena
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)

     # -------------------------- MODULADOR -----------------------------------

    def operador1Mod(self, izq, der):
        op2 = self.op2.tipo
        if self.op1.tipo == TipoDato.ENTERO:
            return self.op2Mod(1, op2, izq, der)
        elif self.op1.tipo == TipoDato.DECIMAL:
            return self.op2Mod(2, op2, izq, der)
        elif self.op1.tipo == TipoDato.BOOLEANO:
            return self.op2Mod(3, op2, izq, der)
        else:
            return Error("Error Sintactico", "Operador invalido", self.linea, self.columna)

    def op2Mod(self, numero, op2, izq, der):
        if numero == 1:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return izq % der
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq) % float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                if str(der).lower() == 'true':
                    return int(izq) % 1
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 2:
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.DECIMAL
                return float(izq) % float(der)
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(izq) % float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.DECIMAL
                if str(der).lower() == 'true':
                    return float(izq) % 1
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        elif numero == 3:
            nuevoIzq = 1 if str(izq).lower() == 'true' else 0
            if op2 == TipoDato.ENTERO:
                self.tipo = TipoDato.ENTERO
                return nuevoIzq % der
            elif op2 == TipoDato.DECIMAL:
                self.tipo = TipoDato.DECIMAL
                return float(nuevoIzq) % float(der)
            elif op2 == TipoDato.BOOLEANO:
                self.tipo = TipoDato.ENTERO
                if str(der).lower() == 'true':
                    return float(izq) % 1
            else:
                return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
