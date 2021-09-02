'''
Byron Orellana
Proyecto JOLC
Segundo semestre 2021
'''
# IMPORTACIONES
# librerias
from controlador.analizador.simbolos.Arbol import Arbol
import ply.yacc as yacc
import ply.lex as lex
# clases propias
from .analizador.expresiones.Aritmetica import Aritmetica
from .analizador.simbolos.Tipo import TipoDato, opAritmetico
from .analizador.expresiones.Nativo import Nativo
from .analizador.instrucciones.Print import Print
from .analizador.instrucciones.Println import Println
from .analizador.excepciones.Error import Error
import re
import sys
sys.setrecursionlimit(3000)

listaErrores = []
input = ''
reservadas = {'print': 'RESPRINT', 'println': 'RESPRINTLN',
              'false': 'RESFALSE', 'true': 'RESTRUE'}
tokens = [
    'PTCOMA', 'MAS', 'MENOS', 'POR', 'DIVI', 'POTENCIA', 'MOD',
    'PARABRE', 'PARCIERRA', 'ENTERO', 'DECIMAL',
    'CARACTER', 'BOOLEANO', 'CADENA', 'IDENTIFICADOR'
] + list(reservadas.values())

# tokens
t_PTCOMA = r';'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVI = r'/'
t_POTENCIA = r'\^'
t_MOD = r'%'
t_PARABRE = r"\("
t_PARCIERRA = r"\)"
t_ignore = ' \t'


def t_nuevaLinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def columnas(entrada, token):
    linea = entrada.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - linea) + 1


def t_error(t):
    listaErrores.append(
        Exception("Lexico", "Existe un error lexico. " + t.value[0],
                  t.lexer.lineno, columnas(input, t)))


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'IDENTIFICADOR')
    return t


def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_CARACTER(t):
    r'\'.?\''
    t.value = t.value[1:-1]
    return t


def t_COMEN_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1


def t_COMEN_MULTI(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')


# analisis lexico
lexer = lex.lex()

# Precedencia de operadores desde el menor hasta el mayor
precedence = (
    # precedencia mas baja
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVI', 'MOD'),
    ('right', 'POTENCIA'),
    ('right', 'UMENOS')
    # precedencia mas alta
)

# IMPORTACIONES
# Definicion de la gramatica


def p_inicio(t):
    'inicio         : instrucciones'
    t[0] = t[1]


def p_instrucciones_instrucciones_i(t):
    'instrucciones          : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t):
    'instrucciones         : instruccion'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]


# INSTRUCCIONES


def p_instruccion(t):
    '''instruccion      : inst_imp PTCOMA
                        | inst_impln PTCOMA 
    '''
    t[0] = t[1]

# error


def p_error(t):
    'instruccion :      error PTCOMA'
    listaErrores.append(Error("Sintactico", "Error de tipo sintactico: " +
                              str(t[1].value), t.lineno(1), columnas(input, t.slice[1])))
    t[0] = ""
# RESULTANTES


def p_inst_imprm(t):
    'inst_imp :      RESPRINT PARABRE expresion PARCIERRA'
    t[0] = Print(t.lineno(1), columnas(input, t.slice[1]), t[3])


def p_inst_imprmln(t):
    'inst_impln :      RESPRINTLN PARABRE expresion PARCIERRA'
    t[0] = Println(t.lineno(1), columnas(input, t.slice[1]), t[3])


# Valores nativos

def p_expresion_lista(t):
    '''
    expresion : expresion MAS expresion
              | expresion MENOS expresion
              | expresion POR expresion
              | expresion DIVI expresion
              | expresion POTENCIA expresion
              | expresion MOD expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(opAritmetico.MAS, t.lineno(
            1), columnas(input, t.slice[2]), t[1], t[3])
    elif t[2] == '-':
        t[0] = Aritmetica(opAritmetico.MENOS, t.lineno(
            1), columnas(input, t.slice[2]), t[1], t[3])
    elif t[2] == '*':
        t[0] = Aritmetica(opAritmetico.POR, t.lineno(
            1), columnas(input, t.slice[2]), t[1], t[3])
    elif t[2] == '/':
        t[0] = Aritmetica(opAritmetico.DIVI, t.lineno(
            1), columnas(input, t.slice[2]), t[1], t[3])
    elif t[2] == '%':
        t[0] = Aritmetica(opAritmetico.MODULO, t.lineno(
            1), columnas(input, t.slice[2]), t[1], t[3])
    elif t[2] == '^':
        t[0] = Aritmetica(opAritmetico.POTENCIA, t.lineno(
            1), columnas(input, t.slice[2]), t[1], t[3])


def p_primitivo_menosU(t):
    '''expresion : MENOS expresion %prec UMENOS'''
    if t[1] == '-':
        t[0] = Aritmetica(opAritmetico.UMENOS, t.lineno(
            1), columnas(input, t.slice[1]), t[2], None)


def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Nativo(
        TipoDato.CADENA,
        t[1], t.lineno(1), columnas(input, t.slice[1])
    )


def p_primitivo_booleanoF(t):
    '''expresion : RESFALSE'''
    t[0] = Nativo(
        TipoDato.BOOLEANO,
        False, t.lineno(1), columnas(input, t.slice[1])
    )


def p_primitivo_booleanoT(t):
    '''expresion : RESTRUE'''
    t[0] = Nativo(
        TipoDato.BOOLEANO,
        True, t.lineno(1), columnas(input, t.slice[1])
    )


def p_primitivo_entero(t):
    '''expresion : ENTERO'''
    t[0] = Nativo(
        TipoDato.ENTERO,
        t[1], t.lineno(1), columnas(input, t.slice[1])
    )


def p_primitivo_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Nativo(
        TipoDato.DECIMAL,
        t[1], t.lineno(1), columnas(input, t.slice[1])
    )


def p_primitivo_carecter(t):
    '''expresion : CARACTER'''
    t[0] = Nativo(
        TipoDato.CARACTER,
        t[1], t.lineno(1), columnas(input, t.slice[1])
    )


def inst_imprmln(t):
    'inst_imp:      RESPRINTLN'


parser = yacc.yacc()


def parse(inp):
    global listaErrores
    global lexer
    listaErrores = []
    lexer = lex.lex(reflags=re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)
