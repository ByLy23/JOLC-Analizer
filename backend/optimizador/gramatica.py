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
from optimizador.analizador.instrucciones.AsignacionDoble import AsignacionDoble
from optimizador.analizador.instrucciones.AsignacionHeapStack import AsignacionHeapStack
from optimizador.analizador.instrucciones.AsignacionSimple import AsignacionSimple
from optimizador.analizador.instrucciones.Encabezado import Encabezado
from optimizador.analizador.instrucciones.Funcion import Funcion
from optimizador.analizador.instrucciones.Goto import Goto
from optimizador.analizador.instrucciones.If import If
from optimizador.analizador.instrucciones.Impresion import Impresion
from optimizador.analizador.instrucciones.Label import Label
from optimizador.analizador.instrucciones.Llamada import Llamada
from optimizador.analizador.instrucciones.Mod import Mod
from optimizador.analizador.instrucciones.ObtenerHeapStack import ObtenerHeapStack
from optimizador.analizador.instrucciones.Return import Return
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
    'fmt': 'RESFMT',
    'math': 'RESMATH',
    'goto': 'RESGOTO',
    'func': 'RESFUNC',
    'Printf': 'RESPRINT',
    'int': 'RESINT',
    'float64': 'RESFLOAT',
    'if': 'RESIF',
    'Mod': 'RESMOD',
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
t_COMPARACION = r'=='
t_IGUAL = r'='
t_MAYOR = r'>'
t_MENOR = r'<'
t_DIFERENTE = r'!='
t_MAYRIGL = r'>='
t_MENRIGL = r'<='
t_PABRE = r"\("
t_PCIERRA = r"\)"
t_CABRE = r"\["
t_CCIERRA = r"\]"
t_LLABRE = r'{'
t_LLCIERRA = r'}'
t_ignore = ' \t'
t_ignore_COMMENT_SIMPLE = r'\#.*\n?'


t_ignore_COMMENT_MULTI = r'\#\=(.|\n)*?\=\#'


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
precedence = (
    #     # precedencia mas baja
    #     # ('left', 'MAYOR', 'MENOR', 'MAYRIGL',
    #     #  'MENRIGL1', 'MENRIGL2', 'COMPARACION', 'DIFERENTE'),
    ('left', 'MAS', 'MENOS'),
    #     # ('left', 'POR', 'DIVI', 'MOD'),
    #     # ('right', 'POTENCIA'),
    ('right', 'UMENOS')
    #     # ('left', 'PUNTO')
    #     # precedencia mas alta
)

# IMPORTACIONES
# Definicion de la gramatica


def p_inicio(t):
    'inicio         :  instrucciones'
    t[0] = t[1]


def p_encabezado(t):
    'encabezado : RESPACKAGE IDENTIFICADOR PTCOMA enviables'
    # print(t[4])
    t[0] = Encabezado(t[4], t.lineno(1), columnas(input, t.slice[1]))


def p_enviables(t):
    'enviables : RESIMPORT PABRE listaImportaciones PCIERRA PTCOMA declaraciones'
    t[0] = {'importaciones': t[3], 'declaraciones': t[6]}

# def p_importaciones(t):
#     'importaciones : RESIMPORT PABRE listaImportaciones PCIERRA PTCOMA'
#     t[0] = []


def p_listaImp(t):
    '''listaImportaciones : listaImportaciones  importacion
    '''
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]


def p_listaImp2(t):
    '''listaImportaciones : importacion
    '''
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]


def p_importacion(t):
    '''importacion : RESFMT
                   | RESMATH
                   | CADENA'''
    t[0] = t[1]


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
    '''declaracion : var_pila  RESFLOAT PTCOMA var_heap  RESFLOAT PTCOMA pila_heap  RESFLOAT PTCOMA temporals RESFLOAT PTCOMA'''
    # print(t[10])
    t[0] = t[10]


def p_pila_heap(t):
    'pila_heap : RESVAR VAR_PILA COMA VAR_HEAP'
    t[0] = []


def p_var_pila(t):
    'var_pila : RESVAR RESSTACK CABRE ENTERO CCIERRA'
    t[0] = []


def p_var_heap(t):
    'var_heap : RESVAR RESHEAP CABRE ENTERO CCIERRA'
    t[0] = []


def p_teimpora(t):
    'temporals : RESVAR temporales'
    t[0] = t[2]


def p_temporales_l(t):
    'temporales : temporales COMA TEMPORAL'
    if t[3] != "":
        t[1].append(t[3])
    t[0] = t[1]


def p_temporales(t):
    'temporales : TEMPORAL'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]


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
                        | inst_mod PTCOMA
                        | encabezado
    '''
    t[0] = t[1]


def p_inst_asig(t):  # asignacion de valores de stack o heap
    'inst_asig : termino CABRE RESINT PABRE termino PCIERRA CCIERRA IGUAL termino '
    t[0] = AsignacionHeapStack(t[1], t[5], t[9], t.lineno(2),
                               columnas(input, t.slice[2]))


def p_inst_asig2(t):
    'inst_asig : termino IGUAL termino CABRE RESINT PABRE termino PCIERRA CCIERRA'
    t[0] = ObtenerHeapStack(t[1], t[3], t[7], t.lineno(2),
                            columnas(input, t.slice[2]))


def p_inst_asig3(t):
    'inst_asig : termino IGUAL termino '
    t[0] = AsignacionSimple(t[1], t[3], t.lineno(2),
                            columnas(input, t.slice[2]))


def p_inst_salto(t):
    'inst_salto : RESGOTO inst_tag'
    t[0] = Goto(t[2], t.lineno(1),
                columnas(input, t.slice[1]))


def p_inst_salto_condi(t):
    'inst_salto_condi : RESIF PABRE termino relacional termino PCIERRA LLABRE RESGOTO inst_tag PTCOMA LLCIERRA'
    t[0] = If(t[3], t[4], t[5], t[9], t.lineno(1), columnas(input, t.slice[1]))


def p_inst_funcion(t):
    'inst_funcion : RESFUNC termino PABRE PCIERRA LLABRE instrucciones LLCIERRA'
    t[0] = Funcion(t[2], t[6], t.lineno(1), columnas(input, t.slice[1]))


def p_inst_llamada(t):
    'inst_llamada : termino PABRE PCIERRA '
    t[0] = Llamada(t[1], t.lineno(2), columnas(input, t.slice[2]))


def p_inst_operacion(t):
    'inst_operacion : termino IGUAL termino operaciones termino '
    t[0] = AsignacionDoble(t[1], t[3], t[4], t[5],
                           t.lineno(2), columnas(input, t.slice[2]))


def p_inst_return(t):
    'inst_return : RESRETURN'
    t[0] = Return(t.lineno(1), columnas(input, t.slice[1]))


def p_inst_impresion(t):
    'inst_impresion : RESFMT PUNTO RESPRINT PABRE CADENA COMA RESINT PABRE termino PCIERRA PCIERRA'
    t[0] = Impresion(t[5], t[9], t.lineno(1), columnas(input, t.slice[1]))


def p_inst_impresion2(t):
    'inst_impresion : RESFMT PUNTO RESPRINT PABRE CADENA COMA  termino PCIERRA'
    t[0] = Impresion(t[5], t[7], t.lineno(1), columnas(input, t.slice[1]))


def p_operaciones(t):
    '''
    operaciones : MAS
                | MENOS
                | POR
                | DIVI
    '''
    t[0] = t[1]


def p_mod(t):
    # {} = math.Mod({},{});\n
    'inst_mod : termino IGUAL RESMATH PUNTO RESMOD PABRE termino COMA termino PCIERRA '
    t[0] = Mod(t[1], t[7], t[9], t.lineno(2),
               columnas(input, t.slice[2]))


def p_relacional(t):
    '''
    relacional : COMPARACION
               | DIFERENTE
               | MENOR
               | MENRIGL
               | MAYOR
               | MAYRIGL
    '''
    t[0] = t[1]
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


def p_termino2(t):
    '''
    termino : MENOS DECIMAL %prec UMENOS
            | MENOS ENTERO  %prec UMENOS
    '''
    # print(t[1], t[2])
    t[2] = "-"+str(t[2])
    t[0] = t[2]


def p_termino(t):
    '''termino : TEMPORAL
                | VAR_PILA
                | VAR_HEAP
                | RESSTACK
                | RESHEAP
                | inst_tag
                | DECIMAL
                | ENTERO
                | IDENTIFICADOR'''
    t[0] = t[1]


def p_inst_tag(t):
    'inst_tag : ETIQUETA'
    t[0] = Label(t[1], t.lineno(1), columnas(input, t.slice[1]))
# error


def p_error(t):
    'instruccion : error PTCOMA'
    if t:
        listaErrores.append(
            Error("Sintactico", "Error de tipo sintactico: " +
                  t.type, t.lineno, t.lexpos))
        print(t.type, t.lineno, t.lexpos)
        parser.restart()
# RESULTANTES


parser = yacc.yacc()


def parse(inp):
    global listaErrores
    global lexer
    listaErrores = []
    # for l in listaErrores:
    #     # print(l)
    lexer = lex.lex(reflags=re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)


def errores():
    lista = listaErrores
    return lista
