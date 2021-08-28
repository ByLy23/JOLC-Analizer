'''
Byron Orellana
Proyecto JOLC
Segundo semestre 2021
'''
# IMPORTACIONES
# librerias
import ply.lex as lex
import ply.yacc as yacc
listaErrores = []
input = ''
reservadas = {
    'print': 'IMPRIMIR',
    'println': 'IMPRIMIRLN'
}
tokens = [
    'PTCOMA',
    'DOSPUNTOS'
    'PARABRE',
    'PARCIERRA',
    'MAS',
    'MENOS',
    'DIVI',
    'POR',
    'ENTERO',
    'DECIMAL',
    'CHAR',
    'BOOLEANO',
    'CADENA',
    'IDENTIFICADOR'
]+list(reservadas.values())

# tokens
t_PTCOMA = r';'
t_DOSPUNTOS = r':'
t_MAS = r'+'
t_MENOS = r"-"
t_POR = r"*"
t_DIVI = r"/"
t_PARABRE = r"("
t_PARCIERRA = r")"
t_igore = " \t"


def t_nuevaLinea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def columnas(entrada, token):
    linea = entrada.rfind('\n', 0, token.lexpos)+1
    return (token.lexpos-linea)+1


def t_error(t):
    listaErrores.append(Exception("Lexico", "Existe un error lexico. " +
                        t.value[0], t.lexer.lineno, columnas(input, t)))


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t


def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'IDENTIFICADOR')
    return t


def t_CADENA(t):
    r'(\".*?\"|\'.*?\')'
    t.value = t.value[1:-1]
    return t


def t_COMEN_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1


# analisis lexico
lexer = lex.lex()

# Precedencia de operadores desde el menor hasta el mayor

precedencia = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVI')
)
