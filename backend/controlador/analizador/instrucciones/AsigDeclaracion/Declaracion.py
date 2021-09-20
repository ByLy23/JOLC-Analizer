from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.reportes.ReporteTabla import ReporteTabla
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Simbolo import Simbolo
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Declaracion(Instruccion):
    def __init__(self, tipo, linea, columna, identificador, valor, struct=None):
        super().__init__(tipo, linea, columna)
        self.identificador = identificador
        self.valor = valor
        self.struct = struct

    def getNodo(self):
        nodo = NodoAST('DECLARACION')
        nodo.agregar(self.identificador)
        if self.valor != None:
            nodo.agregar('=')
            nodo.agregarAST(self.valor.getNodo())
        nodo.agregar(':')
        nodo.agregar(':')
        nodo.agregar(self.tipo)
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        if self.valor == None:  # valor Nothing
            simbolo = Simbolo(self.identificador, self.tipo, None)
            simbolo.tipoStruct = self.struct
            simbolo.mutable = True
            if tablaSimbolo.setVariable(simbolo) != 'La variable existe':
                return Error("Error Semantico", "La variable {} Existe actualmente".format(self.identificador), self.linea, self.columna)
            else:
                if not arbol.actualizarTabla(self.identificador, 'nothing', self.linea, tablaSimbolo.getNombre(), self.columna):
                    nuevoSim = ReporteTabla(self.identificador, 'nothing', 'Variable', str(
                        self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
                    arbol.getSimbolos().append(nuevoSim)
        else:
            val = self.valor.interpretar(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            if self.valor.tipo != self.tipo:
                return Error("Error Semantico", "{} no es compatible con {} ".format(self.valor.tipo, self.tipo), self.linea, self.columna)
            if self.valor.tipo == TipoDato.STRUCT:
                if self.valor.tipoStruct != self.struct:
                    return Error("Error Semantico", "No es el mismo struct", self.linea, self.columna)
            nuevaVal = Simbolo(self.identificador, self.tipo, val)
            nuevaVal.tipoStruct = self.valor.tipoStruct
            nuevaVal.mutable = self.valor.mutable

            if tablaSimbolo.setVariable(nuevaVal) != 'La variable existe':
                return Error("Error Semantico", "La variable {} Existe actualmente".format(self.identificador), self.linea, self.columna)
            else:
                if not arbol.actualizarTabla(self.identificador, val, self.linea, tablaSimbolo.getNombre(), self.columna):
                    nuevoSim = ReporteTabla(self.identificador, val, 'Variable', str(
                        self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
                    arbol.getSimbolos().append(nuevoSim)
