from flask import jsonify
from .analizador.simbolos.Arbol import Arbol
from .analizador.simbolos.TablaSimbolos import TablaSimbolos


def metodoPrincipal(EntradaAnalizar):
    listaErrores = []
    entrada = EntradaAnalizar
    ast = Arbol([])
    tabla = TablaSimbolos([])
    ast.setGlobal(tabla)
    return jsonify(
        {
            "consola": ast.getConsola(),
            "simbolos": ast.getSimbolos(),
            "errores": listaErrores,
        }
    )
