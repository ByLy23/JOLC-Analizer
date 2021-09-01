from enum import Enum


class TipoDato(Enum):
    ENTERO = 1
    DECIMAL = 2
    CADENA = 3
    BOOLEANO = 4
    CARACTER = 5
    VOID = 6  # esto lo tengo que modificar segun la info que me provea el enunciado


class opAritmetico(Enum):
    MAS = 1
    MENOS = 2
    DIVI = 3
    POR = 4
    UMENOS = 5
    MODULO = 6
    POTENCIA = 7
