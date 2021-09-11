from controlador.analizador.instrucciones.funciones.Funcion import Funcion
from controlador.analizador.excepciones.Error import Error
from flask import jsonify
from .analizador.simbolos.Arbol import Arbol
from .analizador.simbolos.TablaSimbolos import TablaSimbolos
from .gramatica import parse


def metodoPrincipal(EntradaAnalizar):
    listaErrores = []
    # try:
    ast = Arbol(parse(EntradaAnalizar))  # entrada con parser
    tabla = TablaSimbolos()
    ast.setGlobal(tabla)
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
    return jsonify(
        {
            "consola": ast.getConsola(),
            "simbolos": ast.getSimbolos(),
            "errores": listaErrores,
        }
    )
    # except:
    #     return jsonify(
    #         {
    #             "consola": "Excepciones ocurridas"
    #         }
    #     )
