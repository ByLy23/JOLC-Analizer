from controlador.analizador.instrucciones.funciones.Funcion import Funcion
from re import S
from controlador.analizador.instrucciones.AsigDeclaracion.Declaracion import Declaracion
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class LlamadaFuncion(Instruccion):
    def __init__(self, identificador, parametros, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.parametros = parametros

    def interpretar(self, arbol, tablaSimbolo):
        funcion = arbol.getFuncion(self.identificador)
        if funcion == None:
            return Error("Error Semantico", "No se encontro la Funcion", self.linea, self.columna)
        if len(funcion.parametros) == len(self.parametros):
            nuevaTabla = TablaSimbolos(tablaSimbolo)
            iterador = 0
            for nuevoVal in self.parametros:
                val = nuevoVal.interpretar(arbol, tablaSimbolo)
                if isinstance(val, Error):
                    return val

                dec = Declaracion(nuevoVal.tipo, funcion.linea,
                                  funcion.columna, funcion.parametros[iterador]["identificador"], nuevoVal)
                nuevaDec = dec.interpretar(arbol, nuevaTabla)
                if isinstance(nuevaDec, Error):
                    return nuevaDec
                var = nuevaTabla.getVariable(
                    funcion.parametros[iterador]["identificador"])
                if var != None:
                    if var.tipo != nuevoVal.tipo:
                        return Error("Semantico", "Tipo de dato diferente", self.linea, self.columna)
                    else:
                        var.setValor(val)
                        nuevaTabla.setNombre(funcion.identificador)
                else:
                    return Error("Error Semantico", "Variable no existe", self.linea, self.columna)
                iterador = iterador+1
            nuevoMet = funcion.interpretar(arbol, nuevaTabla)
            if isinstance(nuevoMet, Error):
                return nuevoMet
            self.tipo = funcion.tipo
            return nuevoMet
        else:
            return Error("Error Semantico", "parametros no coincidientes", self.linea, self.columna)
