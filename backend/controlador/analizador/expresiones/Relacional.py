from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato, opRelacional
from controlador.analizador.abstracto.Instruccion import Instruccion


class Relacional(Instruccion):
    def __init__(self, relacion, cond1, cond2, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.relacion = relacion
        self.cond1 = cond1
        self.cond2 = cond2

    def interpretar(self, arbol, tablaSimbolo):
        izq = self.obtieneValor(self.cond1, arbol, tablaSimbolo)
        if isinstance(izq, Error):
            return izq
        der = self.obtieneValor(self.cond2, arbol, tablaSimbolo)
        if isinstance(der, Error):
            return der
        self.tipo = TipoDato.BOOLEANO
        if self.relacion == opRelacional.IGUAL:
            return izq == der
        elif self.relacion == opRelacional.DIFERENTE:
            return izq != der
        elif self.relacion == opRelacional.MENOR:
            return izq < der
        elif self.relacion == opRelacional.MENORIGUAL:
            return izq <= der
        elif self.relacion == opRelacional.MAYOR:
            return izq > der
        elif self.relacion == opRelacional.MAYORIGUAL:
            return izq >= der
        else:
            return 'Byron lo hizo, si aparece esto en el proyecto de alguien mas es copia sin mi permiso >:v'

    def obtieneValor(self, operando, arbol, tabla):
        valor = operando.interpretar(arbol, tabla)
        if isinstance(valor, Error):
            return valor
        if operando.tipo == TipoDato.ENTERO:
            return int(valor)
        elif operando.tipo == TipoDato.DECIMAL:
            return float(valor)
        elif operando.tipo == TipoDato.CARACTER:
            return chr(ord(valor))
        elif operando.tipo == TipoDato.BOOLEANO:
            return str(valor).lower()
        elif operando.tipo == TipoDato.CADENA:
            return str(valor)
