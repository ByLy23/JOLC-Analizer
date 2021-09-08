'''
Byron Orellana
Proyecto JOLC
Segundo semestre 2021
'''
# IMPORTACIONES
# librerias
from controlador.analizador.instrucciones.ciclica.CondWhile import CondWhile
from controlador.analizador.instrucciones.condicional.CondIf import CondIf
from controlador.analizador.instrucciones.AsigDeclaracion.Asignacion import Asignacion
from controlador.analizador.expresiones.Identificador import Identificador
from controlador.analizador.instrucciones.AsigDeclaracion.Declaracion import Declaracion
from controlador.analizador.expresiones.Relacional import Relacional
import ply.yacc as yacc
import ply.lex as lex
# clases propias
from .analizador.expresiones.Logica import Logica
from .analizador.expresiones.Aritmetica import Aritmetica
from .analizador.simbolos.Tipo import TipoDato, opAritmetico, opLogico, opRelacional
from .analizador.expresiones.Nativo import Nativo
from .analizador.instrucciones.Print import Print
from .analizador.instrucciones.Println import Println
from .analizador.excepciones.Error import Error
import re
import sys
sys.setrecursionlimit(3000)

listaErrores = []
input = ''
reservadas = {
    'print': 'RESPRINT',
    'println': 'RESPRINTLN',
    'false': 'RESFALSE',
    'true': 'RESTRUE',
    'nothing': 'RESNOTHING',
    'Int64': 'RESINT',
    'Float64': 'RESFLOAT',
    'Bool': 'RESBOOL',
    'Char': 'RESCHAR',
    'String': 'RESTRING',
    'if': 'RESIF',
    'else': 'RESELSE',
    'elseif': 'RESELSEIF',
    'end': 'RESEND',
    'while': 'RESWHILE'
}
tokens = [
    'PTCOMA',
    'DOSPUNTOS',
    'MAS',
    'MENOS',
    'POR',
    'DIVI',
    'POTENCIA',
    'MOD',
    'AND',
    'OR',
    'NOT',
    'IGUAL',
    'COMPARACION',
    'DIFERENTE',
    'MAYOR',
    'MENOR',
    'MAYRIGL1',
    'MAYRIGL2',
    'MENRIGL1',
    'MENRIGL2',
    'PARABRE',
    'PARCIERRA',
    'ENTERO',
    'DECIMAL',
    'CARACTER',
    'CADENA',
    'IDENTIFICADOR'
] + list(reservadas.values())

# tokens
t_PTCOMA = r';'
t_DOSPUNTOS = r':'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVI = r'/'
t_NOT = r'!'
t_IGUAL = r'='
t_MAYOR = r'>'
t_MENOR = r'<'
t_COMPARACION = r'=='
t_DIFERENTE = r'!='
t_MAYRIGL1 = r'>='
t_MAYRIGL2 = r'=>'
t_MENRIGL1 = r'<='
t_MENRIGL2 = r'=<'
t_POTENCIA = r'\^'
t_AND = r'&&'
t_OR = r'\|\|'
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
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')
    return t


def t_CADENA(t):
    r'(\".*?\")'
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
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),
    ('left', 'MAYOR', 'MENOR', 'MAYRIGL1', 'MAYRIGL2',
     'MENRIGL1', 'MENRIGL2', 'COMPARACION', 'DIFERENTE'),
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
                        | inst_decla PTCOMA
                        | inst_asig PTCOMA
                        | inst_if RESEND PTCOMA
                        | inst_while RESEND PTCOMA
    '''
    t[0] = t[1]

# error


def p_error(t):
    'instruccion :      error PTCOMA'
    listaErrores.append(Error("Sintactico", "Error de tipo sintactico: " +
                              str(t[1].value), t.lineno(1), columnas(input, t.slice[1])))
    t[0] = ""
# RESULTANTES


def p_inst_while(t):
    'inst_while : RESWHILE expresion instrucciones'
    t[0] = CondWhile(t[2], t[3], t.lineno(1), columnas(input, t.slice[1]))
    # condicion instrucciones


def p_tipo_dato(t):
    '''
    tipodato :           RESINT
                       | RESNOTHING
                       | RESFLOAT
                       | RESTRING
                       | RESCHAR
                       | RESBOOL
    '''
    if t[1].lower() == 'int64':
        t[0] = TipoDato.ENTERO
    elif t[1].lower() == 'nothing':
        t[0] = TipoDato.NOTHING
    elif t[1].lower() == 'float64':
        t[0] = TipoDato.DECIMAL
    elif t[1].lower() == 'string':
        t[0] = TipoDato.CADENA
    elif t[1].lower() == 'char':
        t[0] = TipoDato.CARACTER


def p_inst_if1(t):
    '''inst_if : RESIF expresion instrucciones '''

    t[0] = CondIf(t[2], t[3], [], t.lineno(1), columnas(input, t.slice[1]))
    # fila,columna,cond1,condif,condels,condelseif


def p_inst_if2(t):
    '''inst_if : RESIF expresion instrucciones inst_elif'''

    t[0] = CondIf(t[2], t[3], t[4], t.lineno(1),
                  columnas(input, t.slice[1]))
    # fila,columna,cond1,condif,condels,condelseif


def p_inst_if3(t):
    '''inst_if : RESIF expresion instrucciones RESELSE instrucciones'''

    t[0] = CondIf(t[2], t[3], [{"expresion": None, "instrucciones": t[5]}], t.lineno(1),
                  columnas(input, t.slice[1]))
    # fila,columna,cond1,condif,condels,condelseif


def p_inst_elif(t):
    '''inst_elif : inst_elif elifes'''
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]


def p_inst_elif3(t):
    '''inst_elif : inst_elif RESELSE instrucciones'''
    t[1].append({"expresion": None, "instrucciones": t[3]})
    t[0] = t[1]


def p_inst_elif2(t):
    '''inst_elif : elifes'''
    t[0] = [t[1]]


def p_elifes(t):
    '''elifes : RESELSEIF expresion instrucciones'''
    t[0] = {"expresion": t[2], "instrucciones": t[3]}


def p_inst_asig(t):
    'inst_asig : IDENTIFICADOR IGUAL expresion'
    t[0] = Asignacion(t[1], t[3], t.lineno(1), columnas(input, t.slice[1]))


def p_inst_dec(t):
    '''inst_decla :   IDENTIFICADOR IGUAL expresion DOSPUNTOS DOSPUNTOS tipodato'''
    t[0] = Declaracion(t[6], t.lineno(1), columnas(
        input, t.slice[1]), t[1], t[3])


def p_inst_decN(t):
    '''inst_decla :   IDENTIFICADOR DOSPUNTOS DOSPUNTOS tipodato'''
    t[0] = Declaracion(t[4], t.lineno(1), columnas(
        input, t.slice[1]), t[1], None)


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
              | expresion AND expresion
              | expresion OR expresion
              | expresion MAYOR expresion
              | expresion MENOR expresion
              | expresion MAYRIGL1 expresion
              | expresion MAYRIGL2 expresion
              | expresion MENRIGL1 expresion
              | expresion MENRIGL2 expresion
              | expresion COMPARACION expresion
              | expresion DIFERENTE expresion            
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
    elif t[2] == '&&':
        t[0] = Logica(opLogico.AND, t.lineno(
            1), columnas(input, t.slice[2]), t[1], t[3])
    elif t[2] == '||':
        t[0] = Logica(opLogico.OR, t.lineno(
            1), columnas(input, t.slice[2]), t[1], t[3])
    elif t[2] == '==':
        t[0] = Relacional(opRelacional.IGUAL, t[1], t[3], t.lineno(
            1), columnas(input, t.slice[2]))
    elif t[2] == '!=':
        t[0] = Relacional(opRelacional.DIFERENTE, t[1], t[3], t.lineno(
            1), columnas(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(opRelacional.MAYOR, t[1], t[3], t.lineno(
            1), columnas(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(opRelacional.MENOR, t[1], t[3], t.lineno(
            1), columnas(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(opRelacional.MAYORIGUAL, t[1], t[3], t.lineno(
            1), columnas(input, t.slice[2]))
    elif t[2] == '=>':
        t[0] = Relacional(opRelacional.MAYORIGUAL, t[1], t[3], t.lineno(
            1), columnas(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(opRelacional.MENORIGUAL, t[1], t[3], t.lineno(
            1), columnas(input, t.slice[2]))
    elif t[2] == '=<':
        t[0] = Relacional(opRelacional.MENORIGUAL, t[1], t[3], t.lineno(
            1), columnas(input, t.slice[2]))


def p_primitivo_menosU(t):
    '''expresion : MENOS expresion %prec UMENOS'''
    if t[1] == '-':
        t[0] = Aritmetica(opAritmetico.UMENOS, t.lineno(
            1), columnas(input, t.slice[1]), t[2], None)


def p_primitivo_parentesis(t):
    '''expresion : PARABRE expresion PARCIERRA'''
    t[0] = t[2]


def p_primitivo_negadoU(t):
    '''expresion : NOT expresion %prec UNOT'''
    if t[1] == '!':
        t[0] = Logica(opLogico.NOT, t.lineno(
            1), columnas(input, t.slice[1]), t[2], None)


def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Nativo(
        TipoDato.CADENA,
        t[1], t.lineno(1), columnas(input, t.slice[1])
    )


def p_primitivo_identificador(t):
    '''expresion : IDENTIFICADOR'''
    t[0] = Identificador(t[1], t.lineno(1), columnas(input, t.slice[1])
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
