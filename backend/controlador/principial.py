from controlador.analizador.instrucciones.funciones.Funcion import Funcion
from controlador.analizador.excepciones.Error import Error
from flask import jsonify
from .analizador.simbolos.Arbol import Arbol
from .analizador.simbolos.TablaSimbolos import TablaSimbolos
from .gramatica import errores, parse


def metodoPrincipal(EntradaAnalizar):

    try:
        ast = Arbol(parse(EntradaAnalizar))  # entrada con parser
        tabla = TablaSimbolos()
        ast.setGlobal(tabla)
        listaErrores = errores()
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

        sim = interpretarSimbolos(listaErrores)
        err = interpretarErrores(listaErrores)
        print(err)
        # print(ast.getGlobal())
        return jsonify(
            {
                "consola": ast.getConsola(),
                "simbolos": sim,
                "errores": err,
            }
        )
    except:
        listaErrores = errores()
        err = interpretarErrores(listaErrores)
        print(err)
        return jsonify(
            {
                "consola": "Errores Irrecuperables Encontrados",
                "simbolos": [],
                "errores": err
            }
        )


def interpretarSimbolos(simbolos):
    sim = ""
    return sim


def interpretarErrores(errores):
    err = "["
    iterador = 1
    for error in errores:
        err = err+"{\n"
        err = "{}No:'{}'\nTipo:'{}'\nDescripcion:'{}'\nLinea:'{}'\nColumna:'{}'".format(
            err, iterador, error.tipo, error.descripcion, error.fila, error.columna)
        err = err+"\n},\n"
        iterador += 1
    err = err+"];"
    return err
