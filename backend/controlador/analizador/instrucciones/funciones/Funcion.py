from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.abstracto.Instruccion import Instruccion


class Funcion(Instruccion):
    def __init__(self, tipo, linea, columna, identificador, parametros, instrucciones):
        super().__init__(tipo, linea, columna)
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones

    def interpretar(self, arbol, tablaSimbolo):
        for item in self.instrucciones:
            val = item.interpretar(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            if isinstance(val, Return):
                if(val.valor != None):
                    if self.tipo == val.tipo:
                        return val.valor
                    else:
                        return Error("Error Semantico", "Tipo de datos diferentes", self.linea, self.columna)
                else:
                    return Error('Error Semantico', "La funcion debe devolver un valor", self.linea, self.columna)
