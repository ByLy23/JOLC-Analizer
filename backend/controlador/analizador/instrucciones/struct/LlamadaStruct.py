from controlador.analizador.simbolos.Simbolo import Simbolo
from controlador.analizador.instrucciones.AsigDeclaracion.Declaracion import Declaracion
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class LlamadaStruct(Instruccion):
    def __init__(self, identificador, parametros, linea, columna):
        super().__init__(TipoDato.STRUCT, linea, columna)
        self.identificador = identificador
        self.parametros = parametros

    def interpretar(self, arbol, tablaSimbolo):
        listaStruct = []
        valStruct = arbol.getStruct(self.identificador)
        if valStruct == None:
            return Error("Error Semantico", "La esctructura no existe", self.linea, self.columna)
        # Lista de parametros de struct=valStruct.parametros
        # parametros de la llamada=self.parametros
        if len(valStruct.parametros) != len(self.parametros):
            return Error("Error Semantico", "Cantidad de parametros diferentes", self.linea, self.columna)
        iterador = 0
        for nuevoVal in self.parametros:
            val = nuevoVal.interpretar(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            if valStruct.parametros[iterador]["tipato"] != None:
                if valStruct.parametros[iterador]["tipato"] != nuevoVal.tipo:
                    return Error("Error Semantico", "Tipos de dato diferentes", self.linea, self.columna)
            # se agrega el simbolo de cda parametro del struct
            listaStruct.append(
                Simbolo(valStruct.parametros[iterador]["identificador"], val.tipo, val))
            iterador = iterador+1
        if tablaSimbolo.setVariable(Simbolo(self.identificador, self.tipo, listaStruct)) != 'La variable existe':
            return Error("Error Semantico", "La variable {} Existe actualmente".format(self.identificador), self.linea, self.columna)
