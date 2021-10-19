from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.reportes.ReporteTabla import ReporteTabla
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Identificador(Instruccion):
    def __init__(self, identificador, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.listaAccesos = []

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        variable = tablaSimbolo.getVariable(self.identificador)
        if variable == None:
            return Error("Error Compilacion", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
        self.tipo = variable.tipo
        self.tipoStruct = variable.tipoStruct
        self.mutable = variable.mutable
        # if not arbol.actualizarTabla(self.identificador, variable.valor, self.linea, tablaSimbolo.getNombre(), self.columna):
        #     nuevoSim = ReporteTabla(self.identificador, variable.valor, 'Variable', str(
        #         self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
        #     arbol.getSimbolos().append(nuevoSim)

        if variable.tipo != TipoDato.CADENA and variable.tipo != TipoDato.STRUCT and variable.tipo != TipoDato.ARREGLO:
            temp = arbol.newTemp()
            codigo += arbol.getStack(temp["temporal"], variable.getUbicacion())
            # t1=stack[variable.temporal]
            # return {temporal:t1}
            return {'temporal': temp["temporal"], 'codigo': codigo}
        else:
            temp = arbol.newTemp()
            codigo += arbol.getStack(temp["temporal"], variable.getUbicacion())
            # t1=stack[variable.temporal] devuelve el apuntador del heap
            # return {heap:t1}
            return {'heap': temp["temporal"], 'codigo': codigo}

    def getNodo(self):
        nodo = NodoAST('IDENTIFICADOR')
        nodo.agregar(self.identificador)
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        variable = tablaSimbolo.getVariable(self.identificador)
        if variable == None:
            return Error("Error Semantico", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
        self.tipo = variable.tipo
        self.tipoStruct = variable.tipoStruct
        self.mutable = variable.mutable
        # if not arbol.actualizarTabla(self.identificador, variable.valor, self.linea, tablaSimbolo.getNombre(), self.columna):
        #     nuevoSim = ReporteTabla(self.identificador, variable.valor, 'Variable', str(
        #         self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
        #     arbol.getSimbolos().append(nuevoSim)
        return variable.getValor()
