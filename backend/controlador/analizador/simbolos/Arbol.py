from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.reportes.ReporteTabla import ReporteTabla


class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.consola = ""
        self.funciones = []
        self.tablaGlobal = None
        self.errores = []
        self.listaSimbolos = []
        self.structs = []

    # gets
    def getStructs(self):
        return self.structs

    def getStruct(self, identificador):
        for f in self.structs:
            if identificador == f.identificador:
                # if not self.actualizarTabla(f.identificador, '', f.linea, '', f.columna):
                #     # TODO CAMBIAR TIPO DE DATO XD
                #     nuevoSimbolo = ReporteTabla(f.identificador, '', 'FuncionCreacion', str(
                #         TipoDato.ENTERO), '', f.linea, f.columna)
                #     self.listaSimbolos.append(nuevoSimbolo)
                return f
        return None

    def actualizarTabla(self, ide, valor, linea, entorno, columna):
        for elemento in self.listaSimbolos:
            if elemento.getIdentificador() == ide and elemento.getEntorno() == entorno:
                elemento.setValor(valor)
                elemento.setLinea(linea)
                elemento.setColumna(columna)
                return True
        return False

    def getFuncion(self, identificador):
        for f in self.funciones:
            if identificador == f.identificador:
                # if not self.actualizarTabla(f.identificador, '', f.linea, '', f.columna):
                #     # TODO CAMBIAR TIPO DE DATO XD
                #     nuevoSimbolo = ReporteTabla(f.identificador, '', 'FuncionCreacion', str(
                #         TipoDato.ENTERO), '', f.linea, f.columna)
                #     self.listaSimbolos.append(nuevoSimbolo)
                return f
        return None

    def getSimbolos(self):
        return self.listaSimbolos

    def getErrores(self):
        return self.errores

    def getFunciones(self):
        return self.funciones

    def getInstrucciones(self):
        return self.instrucciones

    def getConsola(self):
        return self.consola

    def getGlobal(self):
        return self.tablaGlobal

    # sets
    def setFunciones(self, funciones):
        self.funciones = funciones

    def setErrores(self, errores):
        self.errores = errores

    def setInstrucciones(self, instruccion):
        self.instrucciones = instruccion

    def setConsola(self, consola):
        self.consola = consola

    def setGlobal(self, tablaGlobal):
        self.tablaGlobal = tablaGlobal

    # actualizarConsola
    def actualizaConsola(self, actualizar):
        self.consola = "{}{}".format(self.consola, str(actualizar))

    def actualizarTabla(self, identificadr, valor, linea, entorno, columna):
        for item in self.listaSimbolos:
            if item.getIdentificador() == identificadr:
                item.setValor(valor)
                item.setLinea(linea)
                item.setEntorno(entorno)
                item.setColumna(columna)
                return True
        return False
