from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.TablaSimbolosC3D import TablaSimbolosC3D
from controlador.analizador.instrucciones.funciones.Funcion import Funcion
from controlador.analizador.excepciones.Error import Error
from .analizador.simbolos.Arbol import Arbol
from .analizador.simbolos.TablaSimbolos import TablaSimbolos
from .gramatica import errores, parse


def metodoPrincipal(EntradaAnalizar):
    err = []
    sim = []
    listaErrores = []
    listaImports = []
    # try:
    ast = Arbol(parse(EntradaAnalizar))  # entrada con parser
    tabla = TablaSimbolos()
    ast.setGlobal(tabla)
    tabla.setNombre('Global')
    astC3D = Arbol(parse(EntradaAnalizar))  # entrada con parser
    tablaC3D = TablaSimbolosC3D()
    astC3D.setGlobal(tablaC3D)
    tablaC3D.setNombre('Global')
    listaErrores = errores()
    for error in listaErrores:
        ast.getErrores().append(error)
        ast.actualizaConsola(error.retornaError())
    for ins in ast.getInstrucciones():
        if isinstance(ins, Funcion):
            ast.getFunciones().append(ins)
    for ins in astC3D.getInstrucciones():
        if isinstance(ins, Funcion):
            astC3D.getFunciones().append(ins)

    traduccionSalida = ""
    for ins in astC3D.getInstrucciones():
        # resultado = ins.interpretar(ast, tabla)
        # if isinstance(resultado, Error):
        #     ast.getErrores().append(resultado)
        #     ast.actualizaConsola(resultado.retornaError())
        if not isinstance(ins, Funcion):
            continue
        else:
            nuevaTablaC3D = TablaSimbolosC3D()
            astC3D.setTempNoUsados([])
            traduccion = ins.traducir(astC3D, nuevaTablaC3D)
            if isinstance(traduccion, Error):
                astC3D.getErrores().append(traduccion)
                astC3D.actualizaConsola(traduccion.retornaError())
                continue

            traduccionSalida += traduccion["codigo"]
    tablaC3D.setTabla({})
    tablaC3D.setTamanio(0)
    astC3D.setTempNoUsados([])
    traduccionSalida += "func main() {\n"
    for ins in astC3D.getInstrucciones():
        if isinstance(ins, Funcion):
            continue
        # resultado = ins.interpretar(ast, tabla)
        # if isinstance(resultado, Error):
        #     ast.getErrores().append(resultado)
        #     ast.actualizaConsola(resultado.retornaError())

        traduccion = ins.traducir(astC3D, tablaC3D)
        if isinstance(traduccion, Error):
            astC3D.getErrores().append(traduccion)
            astC3D.actualizaConsola(traduccion.retornaError())
            continue
        traduccionSalida += traduccion["codigo"]

    traduccionSalida += "\n}"
    if len(astC3D.listaTemporales) > 0:
        tempTraduccion = "var "
        for item in astC3D.listaTemporales:
            tempTraduccion += item+","
        tempTraduccion = tempTraduccion[:-1]
        tempTraduccion += " float64;\n"
        traduccionSalida = tempTraduccion+traduccionSalida

    traduccionSalida = """package main;
import (
   {} 
);\n
var stack [30000000] float64;
var heap [30000000] float64;
var P,H float64;
""".format(astC3D.getImports())+traduccionSalida
    listaSimbolos = astC3D.getSimbolos()

    sim = interpretarSimbolos(listaSimbolos)
    err = interpretarErrores(listaErrores)
    arbol = NodoAST('RAIZ')
    nodoIsnt = NodoAST('INSTRUCCIONES')
    for inst in astC3D.getInstrucciones():
        nodoIsnt.agregarAST(inst.getNodo())
    arbol.agregarAST(nodoIsnt)
    resultado = graficar(arbol)
    # print(ast.getGlobal())
    return {
        "consola2": ast.getConsola(),
        "consola": traduccionSalida,
        "simbolos": sim,
        "errores":  err,
        "ast": resultado
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
        errorTemp = {"No": iterador, "Tipo": error.hora, "Descripcion":
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
