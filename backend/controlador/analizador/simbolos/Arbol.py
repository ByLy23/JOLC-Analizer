class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.consola = ""
        self.funciones = []
        self.tablaGlobal = None
        self.errores = []
        self.listaSimbolos = []

    # gets
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
        self.consola = "{}{}".format(self.consola, actualizar)

    # def actualizarTabla(self,identificadr, valor, linea, entorno, columna):
    #     for item in self.listaSimbolos.keys():
