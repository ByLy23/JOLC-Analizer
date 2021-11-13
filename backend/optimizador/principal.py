from optimizador.analizador.abstracto.Arbol import Arbol
from optimizador.analizador.instrucciones.Encabezado import Encabezado
from optimizador.analizador.instrucciones.Goto import Goto
from .gramatica import errores, parse


def metodoOptimizar(EntradaAnalizar):
    err = []
    opt = []
    listaErrores = []
    listaImports = []
    try:
        codigo = ""
        ast = Arbol(parse(EntradaAnalizar))  # entrada con parser
        for ins in ast.getInstrucciones():
            i = ins.getInstruccion(ast)
            codigo += i
        # for i in ast.getReporte():
            # (self, tipo, descripcion, original, optimizado, linea):
            # print('<--->', i.original, '<--->', i.optimizado)
        # print(ast.getGlobal())
        opt = interpretarOptimizacion(ast.getReporte())
        return {
            "consola": codigo,
            "errores":  err,
            "mirilla": opt
        }

    except:
        listaErrores = errores()
        err = interpretarErrores(listaErrores)
        return {
            "consola": "Errores Irrecuperables Encontrados",
            "simbolos": [],
            "errores": err,
            "ast": []
        }


cuerpo = ''
contador = 0


def interpretarOptimizacion(errores):
    listaFinal = []
    for error in errores:
        errorTemp = {"Tipo": error.tipo, "Regla": error.descripcion, "Original":
                     error.original, "Optimizado": error.optimizado, "Linea": error.linea}
        listaFinal.append(errorTemp)
    return listaFinal


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
