from abc import ABC, abstractmethod


class Instruccion(ABC):
    def __init__(self, tipo, linea, columna):
        self.tipo = tipo
        self.linea = linea
        self.columna = columna
        self.tipoStruct = None  # Trae el nombre del Struct
        self.mutable = False
        self.etiquetaSalida = None
        self.etiquetaContinua = None
        self.etiquetaReturn = None
        self.tempRetorno = None
        super().__init__()

    @abstractmethod
    def interpretar(self, arbol, tablaSimbolo):
        pass

    @abstractmethod
    def getNodo(self):
        pass

    @abstractmethod
    def traducir(self, arbol, tablaSimbolo):
        pass

    def eSalida(self):
        return self.etiquetaSalida

    def eSetSalida(self, s):
        self.etiquetaSalida = s

    def eSetReturn(self, s):
        self.etiquetaReturn = s

    def eContinua(self):
        return self.etiquetaContinua

    def eSetTemporal(self, s):
        self.tempRetorno = s

    def eTemporal(self):
        return self.tempRetorno

    def eReturn(self):
        return self.etiquetaReturn

    def eSetContinua(self, s):
        self.etiquetaContinua = s
