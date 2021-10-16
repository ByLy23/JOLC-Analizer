from controlador.analizador.simbolos.SimboloC3D import SimboloC3D
from .Tipo import TipoDato


class TablaSimbolosC3D:
    def __init__(self, anterior=None):
        self.tablaAnterior = anterior
        self.tablaActual = {}
        # self.funciones=[]
        # self.estructuras=[]
        self.tamanio = 0
        self.tipoDato = TipoDato.ENTERO
        self.nombreDato = ""

    def getTamanio(self):
        return self.tamanio

    def masTamanio(self):
        self.tamanio += 1

    def getAnterior(self):
        return self.tablaAnterior

    def setAnterior(self, anterior):
        self.tablaAnterior = anterior

    def getTabla(self):
        return self.tablaActual

    def setTabla(self, tabla):
        self.tablaActual = tabla

    def setVariable(self, simbolo):
        if simbolo.getIdentificador() in self.tablaActual:
            return "La variable {} existe ya".format(simbolo.getIdentificador())
        else:
            self.tablaActual[simbolo.getIdentificador()] = simbolo
            if simbolo.esStack:
                self.tamanio += 1
        return 'La variable existe'
        # aux = self
        # while aux != None:
        #     if simbolo.getIdentificador() in aux.tablaActual:
        #         return aux.tablaActual[simbolo.getIdentificador()]
        #     else:
        #         aux = aux.tablaAnterior
        # return 'La variable existe'

    def getVariable(self, id):
        aux = self
        while aux != None:
            if id in aux.tablaActual:
                return aux.tablaActual[id]
            else:
                aux = aux.tablaAnterior
        return None

    def getVariableGlobal(self, id):
        aux = self
        if id in aux.tablaActual:
            return aux.tablaActual[id]
        return None

    def getNombre(self):
        return self.nombreDato

    def setNombre(self, nombre):
        self.nombreDato = nombre
