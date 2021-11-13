from optimizador.analizador.abstracto.Instruccion import Instruccion
from optimizador.analizador.abstracto.Reporte import Reporte


class AsignacionDoble(Instruccion):
    def __init__(self, temp, t1, op, t2, linea, columna):
        super().__init__(linea, columna)
        self.temp = str(temp)
        self.t1 = str(t1)
        self.t2 = str(t2)
        self.op = str(op)

    def getInstruccion(self, arbol):
        aux = '{} = {} {} {};\n'.format(self.temp, self.t1, self.op, self.t2)
        if(self.temp == self.t1):  # reglas 8, 9,10,11 estas las saque de un pdf que tenia codigos xd pero en el enunciado lo resumen a la regla 6, 7 y 8, pal que lea esto si lo lee xd
            # if self.temp == "t12":
            # print(self.t2 == "0")
            if self.t2 == ('0', '0.0'):  # regla 8 y 9
                if self.op == ('+', '-'):
                    reporte = Reporte('Mirilla Simplificación algebraica y por fuerza', 'Regla 6', aux,
                                      '{} = {} {} 0; se elimina'.format(self.temp, self.temp, self.op), self.linea)
                    arbol.getReporte().append(reporte)
                    return ''
            if self.t2 == ('1', '1.0'):  # Reglas 10 y 11
                if self.op == ('*', '/'):
                    reporte = Reporte('Mirilla Simplificación algebraica y por fuerza', 'Regla 6', aux,
                                      '{} = {} {} 0; se elimina'.format(self.temp, self.temp, self.op), self.linea)
                    arbol.getReporte().append(reporte)
                    return ''
        else:  # Reglas 12,13,14,15,16,17,18
            if self.t1 == ('0', '0.0'):  # regla 18
                if self.op == "/":
                    reporte = Reporte('Mirilla Simplificación algebraica y por fuerza', 'Regla 8', aux,
                                      '{} = 0.0;'.format(self.temp), self.linea)
                    arbol.getReporte().append(reporte)
                    return '{} = 0.0;\n'.format(self.temp)
            if (self.t2, self.t1) == ('0', '0.0'):  # regla 12 y 13
                if self.op == ('+', '-'):
                    reporte = Reporte('Mirilla Simplificación algebraica y por fuerza', 'Regla 7', aux,
                                      '{} = {};'.format(self.temp, self.t1), self.linea)
                    arbol.getReporte().append(reporte)
                    return '{} = {};\n'.format(self.temp, self.t1)
                elif self.op == "*":  # Regla 17
                    reporte = Reporte('Mirilla Simplificación algebraica y por fuerza', 'Regla 8', aux,
                                      '{} = 0.0;'.format(self.temp), self.linea)
                    arbol.getReporte().append(reporte)
                    return '{} = 0.0;\n'.format(self.temp)
            elif self.t2 == ('1', '1.0'):  # Reglas 14 y 15
                if self.op == ('*', '/'):
                    reporte = Reporte('Mirilla Simplificación algebraica y por fuerza', 'Regla 7', aux,
                                      '{} = {};'.format(self.temp, self.t1), self.linea)
                    arbol.getReporte().append(reporte)
                    return '{} = {};\n'.format(self.temp, self.t1)
            elif self.t2 == "2.0" or self.t2 == "2":  # Regla 16
                if self.op == "*":
                    reporte = Reporte('Mirilla Simplificación algebraica y por fuerza', 'Regla 8', aux, '{} = {} + {};'.format(
                        self.temp, self.t1, self.t1), self.linea)
                    arbol.getReporte().append(reporte)
                    return '{} = {} + {};\n'.format(self.temp, self.t1, self.t1)

        return aux

    def getNormal(self):
        return '{} = {} {} {};\n'.format(self.temp, self.t1, self.op, self.t2)
