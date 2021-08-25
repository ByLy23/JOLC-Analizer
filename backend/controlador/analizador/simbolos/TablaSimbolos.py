from .Tipo import TipoDato
from .Simbolo import Simbolo


class TablaSimbolos:
    def __init__(self, anterior=None):
        self.tablaAnterior = anterior
        self.tablaActual = {}
        self.tipoDato = TipoDato.ENTERO
        self.nombreDato = ""

    def getAnterior(self):
        return self.tablaAnterior

    def setAnterior(self, anterior):
        self.tablaAnterior = anterior

    def getTabla(self):
        return self.tablaActual

    def setTabla(self, tabla):
        self.tablaActual = tabla

    def setVariable(self, simbolo):
        aux = self
        while aux != None:
            found = aux.getTabla().get(simbolo.getIdentificador())
            if found != None:
                return 'La variable existe'
            aux = aux.getAnterior()
        self.tablaActual.setdefault(simbolo.getIdentificador(), simbolo)
        return 'creada con exito'

    def getVariable(self, id):
        aux = self
        while aux != None:
            found = aux.getTabla().get(id)
            if found != None:
                return found
            aux = aux.getAnterior()
        return None

    def getNombre(self):
        return self.nombreDato

    def setNombre(self, nombre):
        self.nombreDato = nombre
