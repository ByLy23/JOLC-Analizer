
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
        if operador == opAritmetico.UMENOS:
            self.operadorUnico = op1
        else:
            self.op1 = op1
            self.op2 = op2

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
        elif self.operador == opAritmetico.POTENCIA:
            return self.operador1Potencia(izq, der)
        elif self.operador == opAritmetico.MODULO:
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
