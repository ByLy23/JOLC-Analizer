from datetime import datetime


class Error:
    def __init__(self, tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        now = datetime.now()
        self.hora = now.strftime("%d/%m/%Y %H:%M:%S")

    def retornaError(self):

        return str("Error de tipo: {} {} en la linea: {} y columna: {} \n".format(
            self.tipo, self.descripcion, self.fila, self.columna
        ))
