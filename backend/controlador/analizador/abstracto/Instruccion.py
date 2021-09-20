from abc import ABC, abstractmethod


class Instruccion(ABC):
    def __init__(self, tipo, linea, columna):
        self.tipo = tipo
        self.linea = linea
        self.columna = columna
        self.tipoStruct = None  # Trae el nombre del Struct
        self.mutable = False
        super().__init__()

    @abstractmethod
    def interpretar(self, arbol, tablaSimbolo):
        pass

    @abstractmethod
    def getNodo(self):
        pass
