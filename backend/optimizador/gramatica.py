'''
Byron Orellana
Proyecto JOLC
Segundo semestre 2021
'''
# IMPORTACIONES
# librerias

import ply.yacc as yacc
import ply.lex as lex
# clases propias

import re
import sys

from controlador.analizador.excepciones.Error import Error
sys.setrecursionlimit(5000)
listaErrores = []
input = ''
reservadas = {
    'stack': 'RESSTACK',
    'heap': 'RESHEAP',
    'P': 'VAR_PILA',
    'H': 'VAR_HEAP',
    'var': 'RESVAR',
    'import': 'RESIMPORT',
    'package': 'RESPACKAGE',
    'main': 'RESMAIN',
    'fmt': 'RESFMT',
    'math': 'RESMATH',
    'goto': 'RESGOTO',
    'func': 'RESFUNC',
    'Printf': 'RESPRINT',
    'int': 'RESINT',
    'float64': 'RESFLOAT',
    'if': 'RESIF',
    '%c': 'VALCHAR',
    '%f': 'VALFLOAT',
    '%d': 'VALDIGIT',
    'mod': 'RESMOD',
    'return': 'RESRETURN'
}
tokens = [
    'DOSPUNTOS',
    'PTCOMA',
    'PUNTO',
    'ETIQUETA',
    'TEMPORAL',
    'LLABRE',
    'LLCIERRA',
    'CABRE',
    'CCIERRA',
    'MAS',
    'MENOS',
    'POR',
    'DIVI',
    'MOD',
    'POTENCIA',
    'PABRE',
    'PCIERRA',
    'MAYOR',
    'MENOR',
    'MAYRIGL',
    'MENRIGL',
    'IGUAL',
    'COMPARACION',
    'DIFERENTE',
    'COMA',
    'IDENTIFICADOR',
    'COMM_SIMPLE',
    'ENTERO',
    'DECIMAL',
    'CADENA'
] + list(reservadas.values())

# tokens
t_PTCOMA = r';'
t_DOSPUNTOS = r':'
t_MAS = r'\+'
t_PUNTO = r'\.'
t_COMA = r','
t_MENOS = r'-'
t_POR = r'\*'
t_DIVI = r'/'
t_IGUAL = r'='
t_MAYOR = r'>'
t_MENOR = r'<'
t_COMPARACION = r'=='
t_DIFERENTE = r'!='
t_MAYRIGL = r'>='
t_MENRIGL = r'<='
t_POTENCIA = r'\^'
t_MOD = r'%'
t_PABRE = r"\("
t_PCIERRA = r"\)"
t_CABRE = r"\["
t_CCIERRA = r"\]"
t_LLABRE = r'{'
t_LLCIERRA = r'}'
t_ignore = ' \t'
t_ignore_COMMENT_SIMPLE = r'\/\/.*\n?'
t_ignore_COMMENT_MULTI = r'\/\*(.|\n)*?\*\/'


def t_nuevaLinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def columnas(entrada, token):
    linea = entrada.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - linea) + 1


def t_error(t):
    listaErrores.append(Error("Lexico", "Token: \" {} \" no pertenece al lenguaje".format(
        t.value[0]), t.lexer.lineno, columnas(input, t)))

    t.lexer.skip(1)


def t_TEMPORAL(t):
    r't\d+'
    t.type = reservadas.get(t.value, 'TEMPORAL')
    return t


def t_ETIQUETA(t):
    r'L\d+'
    t.type = reservadas.get(t.value, 'ETIQUETA')
    return t


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


def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1]
    return t


def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')
    return t


# analisis lexico
lexer = lex.lex()

# Precedencia de operadores desde el menor hasta el mayor
# precedence = (
#     # precedencia mas baja
#     ('left', 'MAYOR', 'MENOR', 'MAYRIGL',
#      'MENRIGL1', 'MENRIGL2', 'COMPARACION', 'DIFERENTE'),
#     ('left', 'MAS', 'MENOS'),
#     ('left', 'POR', 'DIVI', 'MOD'),
#     ('right', 'POTENCIA'),
#     ('right', 'UMENOS'),
#     ('left', 'PUNTO')
#     # precedencia mas alta
# )

# IMPORTACIONES
# Definicion de la gramatica


def p_inicio(t):
    'inicio         : encabezado instrucciones'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[2]


def p_encabezado(t):
    'encabezado : paquete importaciones declaraciones'


def p_paquete(t):
    'paquete : RESPACKAGE RESMAIN PTCOMA'


def p_importaciones(t):
    'importaciones : RESIMPORT PABRE listaImportaciones PCIERRA PTCOMA'


def p_listaImp(t):
    '''listaImportaciones : RESFMT
                            | RESMATH
                            | CADENA
    '''


def p_declaraciones(t):
    'declaraciones : declaraciones declaracion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[2]


def p_declaracion1(t):
    'declaraciones : declaracion'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]


def p_declaracion(t):
    '''declaracion : temporals RESFLOAT PTCOMA
                    | pila_heap  RESFLOAT PTCOMA
                    | var_pila  RESFLOAT PTCOMA
                    | var_heap  RESFLOAT PTCOMA'''
    t[0] = t[1]


def p_pila_heap(t):
    'pila_heap : RESVAR VAR_PILA COMA VAR_HEAP'


def p_var_pila(t):
    'var_pila : RESVAR RESSTACK CABRE ENTERO CCIERRA'


def p_var_heap(t):
    'var_heap : RESVAR RESHEAP CABRE ENTERO CCIERRA'


def p_teimpora(t):
    'temporals : RESVAR temporales'
    t[0] = t[2]


def p_temporales(t):
    'temporales : TEMPORAL'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]


def p_temporales_l(t):
    'temporales : temporales COMA TEMPORAL'
    if t[2] != "":
        t[1].append(t[2])
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
    '''instruccion      : inst_asig PTCOMA
                        | inst_salto PTCOMA
                        | inst_salto_condi 
                        | inst_funcion
                        | inst_llamada PTCOMA
                        | inst_operacion PTCOMA
                        | inst_return PTCOMA
                        | inst_impresion PTCOMA
                        | inst_tag DOSPUNTOS
    '''
    t[0] = t[1]


def p_inst_asig(t):  # asignacion de valores de stack o heap
    'inst_asig : termino CABRE RESINT PABRE termino PCIERRA CCIERRA IGUAL termino '


def p_inst_asig2(t):
    'inst_asig : termino IGUAL termino CABRE RESINT PABRE termino PCIERRA CCIERRA'


def p_inst_asig3(t):
    'inst_asig : termino IGUAL termino '


def p_inst_salto(t):
    'inst_salto : RESGOTO ETIQUETA'


def p_inst_salto_condi(t):
    'inst_salto_condi : RESIF PABRE termino relacional termino PCIERRA LLABRE RESGOTO ETIQUETA PTCOMA LLCIERRA'


def p_inst_salto_condi(t):
    'inst_salto_condi : RESIF  termino relacional termino PCIERRA LLABRE RESGOTO ETIQUETA PTCOMA LLCIERRA'


def p_inst_funcion(t):
    'inst_funcion : RESFUNC IDENTIFICADOR PABRE PCIERRA LLABRE instrucciones LLCIERRA'


def p_inst_llamada(t):
    'inst_llamada : IDENTIFICADOR PABRE PCIERRA '


def p_inst_operacion(t):
    'inst_operacion : termino IGUAL termino operaciones termino '


def p_inst_return(t):
    'inst_return : RESRETURN'


def p_inst_impresion(t):
    'inst_impresion : RESFMT PUNTO RESPRINT PABRE CADENA COMA RESINT PABRE ENTERO PCIERRA PCIERRA'


def p_inst_impresion2(t):
    'inst_impresion : RESFMT PUNTO RESPRINT PABRE CADENA COMA RESINT PABRE TEMPORAL PCIERRA PCIERRA'


def p_operaciones(t):
    '''
    operaciones : MAS
                | MENOS
                | POR 
                | DIVI
                | MOD
    '''


def p_relacional(t):
    '''
    relacional : COMPARACION
               | DIFERENTE
               | MENOR
               | MENRIGL
               | MAYOR
               | MAYRIGL
    '''
    # if t[2] == '+':
    #     t[0] = Aritmetica(opAritmetico.MAS, t.lineno(
    #         2), columnas(input, t.slice[2]), t[1], t[3])
    # elif t[2] == '-':
    #     t[0] = Aritmetica(opAritmetico.MENOS, t.lineno(
    #         2), columnas(input, t.slice[2]), t[1], t[3])
    # elif t[2] == '*':
    #     t[0] = Aritmetica(opAritmetico.POR, t.lineno(
    #         2), columnas(input, t.slice[2]), t[1], t[3])
    # elif t[2] == '/':
    #     t[0] = Aritmetica(opAritmetico.DIVI, t.lineno(
    #         2), columnas(input, t.slice[2]), t[1], t[3])
    # elif t[2] == '%':
    #     t[0] = Aritmetica(opAritmetico.MODULO, t.lineno(
    #         2), columnas(input, t.slice[2]), t[1], t[3])
    # elif t[2] == '^':
    #     t[0] = Aritmetica(opAritmetico.POTENCIA, t.lineno(
    #         2), columnas(input, t.slice[2]), t[1], t[3])


def p_termino(t):
    'termino : TEMPORAL'


def p_termino2(t):
    'termino : VAR_PILA'


def p_termino3(t):
    'termino : VAR_HEAP'


def p_termino4(t):
    'termino : RESSTACK'


def p_termino5(t):
    'termino : RESHEAP'


def p_termino6(t):
    'termino : DECIMAL'


def p_termino7(t):
    'termino : ENTERO'


def p_termino8(t):
    'termino : IDENTIFICADOR'


def p_inst_tag(t):
    'inst_tag : ETIQUETA'
    t[0] = t[1]
# error


def p_error(t):
    'instruccion : error PTCOMA'
    if t:
        listaErrores.append(
            Error("Sintactico", "Error de tipo sintactico: " +
                  t.type, t.lineno, t.lexpos))
        print(listaErrores)
        parser.restart()
# RESULTANTES


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


def errores():
    lista = listaErrores
    return lista
