from controlador.analizador.excepciones.Error import Error
from flask import jsonify
from .analizador.simbolos.Arbol import Arbol
from .analizador.simbolos.TablaSimbolos import TablaSimbolos
from .gramatica import parse
import json


def metodoPrincipal(EntradaAnalizar):
    listaErrores = []
    ast = Arbol(parse(EntradaAnalizar))  # entrada con parser
    tabla = TablaSimbolos([])
    ast.setGlobal(tabla)
    for ins in ast.getInstrucciones():
        resultado = ins.interpretar(ast, tabla)
        if isinstance(resultado, Error):
            listaErrores.append(resultado)
            ast.getErrores().append(resultado)
            ast.actualizaConsola(resultado.retornaError())
    return jsonify(
        {
            "consola": ast.getConsola(),
            "simbolos": ast.getSimbolos(),
            "errores": listaErrores,
        }
    )
