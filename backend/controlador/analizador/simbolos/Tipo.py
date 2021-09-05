from enum import Enum


class TipoDato(Enum):
    ENTERO = 1
    DECIMAL = 2
    CADENA = 3
    BOOLEANO = 4
    CARACTER = 5
    NOTHING = 6


class opAritmetico(Enum):
    MAS = 1
    MENOS = 2
    DIVI = 3
    POR = 4
    UMENOS = 5
    MODULO = 6
    POTENCIA = 7


class opLogico(Enum):
    AND = 1
    OR = 2
    NOT = 3


class opRelacional(Enum):
    IGUAL = 1
    DIFERENTE = 2
    MAYOR = 3
    MENOR = 4
    MAYORIGUAL = 5
    MENORIGUAL = 6
