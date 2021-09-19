from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.instrucciones.funciones.Funcion import Funcion
from controlador.analizador.excepciones.Error import Error
import json
from .analizador.simbolos.Arbol import Arbol
from .analizador.simbolos.TablaSimbolos import TablaSimbolos
from .gramatica import errores, parse


def metodoPrincipal(EntradaAnalizar):
    err = []
    sim = []
    listaErrores = []
    # try:
    ast = Arbol(parse(EntradaAnalizar))  # entrada con parser
    tabla = TablaSimbolos()
    ast.setGlobal(tabla)
    tabla.setNombre('Global')
    listaErrores = errores()
    for error in listaErrores:
        ast.getErrores().append(error)
        ast.actualizaConsola(error.retornaError())
    for ins in ast.getInstrucciones():
        if isinstance(ins, Funcion):
            ast.getFunciones().append(ins)
    for ins in ast.getInstrucciones():
        if isinstance(ins, Funcion):
            continue
        resultado = ins.interpretar(ast, tabla)
        if isinstance(resultado, Error):
            ast.getErrores().append(resultado)
            ast.actualizaConsola(resultado.retornaError())
    listaSimbolos = ast.getSimbolos()
    sim = interpretarSimbolos(listaSimbolos)
    err = interpretarErrores(listaErrores)
    # print(ast.getGlobal())
    return {
        "consola": ast.getConsola(),
        "simbolos": sim,
        "errores":  err,
    }

    # except:
    #     listaErrores = errores()
    #     err = interpretarErrores(listaErrores)
    #     return jsonify(
    #         {
    #             "consola": "Errores Irrecuperables Encontrados",
    #             "simbolos": [],
    #             "errores": err
    #         }
    #     )


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
    # iterador = 1
    # sim = ''
    # for simbolo in simbolos:
    #     if str(simbolo.tipo)[9:] == 'NOTHING':
    #         simbolo.tipo = 'TipoDato.FUNCION'
    #     sim += 'No:{},Nombre:{},Tipo:{},Entorno:{},Linea:{},Columna:{}'.format(
    #         iterador, simbolo.identificador, str(simbolo.tipo)[9:].capitalize(), simbolo.entorno, simbolo.linea, simbolo.columna)
    #     sim += '},'
    #     iterador += 1
    # if sim != '':
    #     sim = sim[0:-1:1]
    # print(sim)
    # return sim


def interpretarErrores(errores):
    listaFinal = []
    iterador = 1
    for error in errores:
        errorTemp = {"No": iterador, "Tipo": error.tipo, "Descripcion":
                     error.descripcion, "Linea": error.fila, "Columna": error.columna}
        listaFinal.append(errorTemp)
        iterador += 1
    return listaFinal
    # err = ""
    # iterador = 1
    # for error in errores:
    #     err = err+"{"
    #     err = "{}No:'{}',Tipo:'{}',Descripcion:'{}',Linea:'{}',Columna:'{}'".format(
    #         err, iterador, error.tipo, error.descripcion, error.fila, error.columna)
    #     err = err+"},"
    #     iterador += 1
    # if err != "":
    #     err = err[0:-1:1]
    # return err
