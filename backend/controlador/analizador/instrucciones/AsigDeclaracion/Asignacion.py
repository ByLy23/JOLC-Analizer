from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.reportes.ReporteTabla import ReporteTabla
from controlador.analizador.simbolos.Simbolo import Simbolo
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Asignacion(Instruccion):
    def __init__(self, tipoAsignacion, identificador, valor, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.tipoAsignacion = tipoAsignacion
        self.valor = valor

    def getNodo(self):
        nodo = NodoAST('ASIGNACION')
        if self.tipoAsignacion != None:
            nodo.agregar(self.tipoAsignacion)
        nodo.agregar(self.identificador)
        nodo.agregar('=')
        if self.valor != None:
            nodo.agregarAST(self.valor.getNodo())
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):

        variable = tablaSimbolo.getVariable(self.identificador)
        if variable != None:
            if self.valor != None:
                val = self.valor.interpretar(arbol, tablaSimbolo)
                if not variable.mutable:

                    if variable.tipo != TipoDato.NOTHING and variable.tipo != self.valor.tipo:
                        return Error("Error Semantico", "Variable {} con tipo de dato diferente".format(self.identificador), self.linea, self.columna)
                    else:
                        variable.setValor(val)
                        variable.setTipo(self.valor.tipo)
                        variable.tipoStruct = self.valor.tipoStruct
                        variable.mutable = self.valor.mutable

                else:
                    variable.setValor(val)
                    variable.tipo = self.valor.tipo
                    variable.tipoStruct = self.valor.tipoStruct
                    variable.mutable = self.valor.mutable
                if not arbol.actualizarTabla(self.identificador, val, self.linea, tablaSimbolo.getNombre(), self.columna):
                    nuevoSim = ReporteTabla(self.identificador, val, 'Variable', str(
                        self.valor.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
                    arbol.getSimbolos().append(nuevoSim)
        else:
            val = self.valor.interpretar(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            nuevoSimbolo = Simbolo(
                self.identificador, self.valor.tipo, val)
            nuevoSimbolo.tipoStruct = self.valor.tipoStruct
            nuevoSimbolo.mutable = True
            if tablaSimbolo.setVariable(nuevoSimbolo) != 'La variable existe':
                return Error("Error Semantico", "La variable {} Existe actualmente".format(self.identificador), self.linea, self.columna)
            else:
                if not arbol.actualizarTabla(self.identificador, val, self.linea, tablaSimbolo.getNombre(), self.columna):
                    nuevoSim = ReporteTabla(self.identificador, val, 'Variable', str(
                        self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
                    arbol.getSimbolos().append(nuevoSim)
