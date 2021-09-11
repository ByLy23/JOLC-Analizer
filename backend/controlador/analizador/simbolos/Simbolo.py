class Simbolo:
    def __init__(self, identificador, tipo, valor=None):
        self.identificador = identificador
        self.tipo = tipo
        self.valor = valor
        self.tipoStruct = None  # Trae el nombre del Struct

    def getTipo(self):
        return self.tipo

    def getIdentificador(self):
        return self.identificador

    def getValor(self):
        return self.valor

    def setTipo(self, tipo):
        self.tipo = tipo

    def setIdentificador(self, identificador):
        self.identificador = identificador

    def setValor(self, valor):
        self.valor = valor
