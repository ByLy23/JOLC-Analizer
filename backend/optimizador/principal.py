from optimizador.analizador.abstracto.Arbol import Arbol
from .gramatica import errores, parse


def metodoOptimizar(EntradaAnalizar):
    err = []
    sim = []
    listaErrores = []
    listaImports = []
    # try:
    codigo = ""
    ast = Arbol(parse(EntradaAnalizar))  # entrada con parser
    for ins in ast.getInstrucciones():
        i = ins.getInstruccion(ast)
        codigo += i
    # print(ast.getGlobal())
    return {
        "consola": codigo,
        "simbolos": sim,
        "errores":  err,
    }

    # except:
    #     listaErrores = errores()
    #     err = interpretarErrores(listaErrores)
    #     return {
    #         "consola": "Errores Irrecuperables Encontrados",
    #         "simbolos": [],
    #         "errores": err,
    #         "ast": []
    #     }


cuerpo = ''
contador = 0


def graficar(arbol):
    res = ''
    global cuerpo
    global contador
    cuerpo = ''
    contador = 1
    graphAST('n0', arbol)
    res = 'digraph arbolAST'
    res += '{'
    res += '\nn0[label="{}"];\n{}'.format(
        arbol.getValor(), cuerpo)
    res += '}'
    return res


def graphAST(texto, padre):
    global cuerpo
    global contador
    for hijo in padre.getHijos():
        nombreHijo = 'n{}'.format(contador)
        cuerpo += '{}[label="{}"];\n{} -> {};\n'.format(
            nombreHijo, hijo.getValor(), texto, nombreHijo)
        contador += 1
        graphAST(nombreHijo, hijo)


def interpretarSimbolos(simbolos):
    listaFinal = []
    iterador = 1
    for simbolo in simbolos:
        if str(simbolo.tipo)[9:] == 'NOTHING':
            simbolo.tipo = 'TipoDato.FUNCION'
        simboloTemp = {"No": iterador, "Nombre": simbolo.identificador, "Tipo": str(
            simbolo.tipo)[9:], "Entorno": simbolo.entorno, "Linea": simbolo.linea, "Columna": simbolo.columna}
        listaFinal.append(simboloTemp)
        iterador += 1
    return listaFinal


def interpretarErrores(errores):
    listaFinal = []
    iterador = 1
    for error in errores:
        errorTemp = {"No": iterador, "Tipo": error.hora, "Descripcion":
                     error.descripcion, "Linea": error.fila, "Columna": error.columna}
        listaFinal.append(errorTemp)
        iterador += 1
    return listaFinal
