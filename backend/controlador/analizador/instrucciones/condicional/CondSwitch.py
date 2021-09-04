from controlador.analizador.abstracto.Instruccion import Instruccion


class CondSwitch(Instruccion):
    def __init__(self, tipo, linea, columna):
        super().__init__(tipo, linea, columna)
