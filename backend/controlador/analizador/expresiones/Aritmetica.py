
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato, opAritmetico
from controlador.analizador.abstracto.Instruccion import Instruccion


class Aritmetica(Instruccion):
    def __init__(self, operador,  linea, columna, op1, op2=None):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.operador = operador
        if operador == opAritmetico.UMENOS:
            self.operadorUnico = op1
        else:
            self.op1 = op1
            self.op2 = op2

    def interpretar(self, arbol, tablaSimbolo):
        izq = der = uno = None
        if self.operadorUnico != None:
            uno = self.operadorUnico.interpretar(arbol, tablaSimbolo)
            if isinstance(uno, Error):
                return uno
        else:
            izq = self.op1.interpretar(arbol, tablaSimbolo)
            if isinstance(izq, Error):
                return izq
            der = self.op2.interpretar(arbol, tablaSimbolo)
            if isinstance(der, Error):
                return der
        if self.operador == opAritmetico.MAS:
            return self.operador1Suma(izq, der)
        elif self.operador == opAritmetico.MENOS:
            return self.operador1Resta(izq, der)
        elif self.operador == opAritmetico.POR:
            print(izq)
            # return self.operador1Multi(izq,der)
        elif self.operador == opAritmetico.DIVI:
            print(izq)
            # return self.operador1Division(izq,der)
        elif self.operador == opAritmetico.POTENCIA:
            print(izq)
            # return self.operador1Potencia(izq,der)
        elif self.operador == opAritmetico.MODULO:
            print(izq)
            # return self.operador1Mod(izq,der)
        elif self.operador == opAritmetico.UMENOS:
            print(uno)
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
                return izq - der
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
        # elif numero == 4:
        #     nuevoIzq = ord(str(izq))
        #     if op2 == TipoDato.ENTERO:
        #         self.tipo = TipoDato.CARACTER
        #         return chr(nuevoIzq + der)
        #     elif op2 == TipoDato.BOOLEANO:
        #         self.tipo = TipoDato.CARACTER
        #         return chr(nuevoIzq+1 if str(der).lower() == 'true' else nuevoIzq)
        #     else:
        #         return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
        else:
            return Error("Error Sintactico", "Tipo de dato incompatible", self.linea, self.columna)
