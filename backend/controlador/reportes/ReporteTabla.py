class ReporteTabla():
    def __init__(self, ide, valor, forma, tipo, entorno, linea, columna):
        self.identificador = ide
        self.forma = forma
        self.tipo = tipo
        self.entorno = entorno
        self.linea = linea
        self.columna = columna
        self.valor = valor

    def getIdentificador(self):
        return self.identificador

    def getForma(self):
        return self.forma

    def getTipo(self):
        return self.tipo

    def getEntorno(self):
        return self.entorno

    def getLinea(self):
        return self.linea

    def getColumna(self):
        return self.columna

    def getValor(self):
        return self.valor

    def setLinea(self, linea):
        self.linea = linea

    def setColumna(self, col):
        self.columna = col

    def setValor(self, val):
        self.valor = val

    def setEntorno(self, ent):
        self.entorno = ent
