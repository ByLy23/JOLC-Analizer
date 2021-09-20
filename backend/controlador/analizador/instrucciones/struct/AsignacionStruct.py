from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.reportes.ReporteTabla import ReporteTabla
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class AsignacionStruct(Instruccion):
    def __init__(self, identificador, parametro, expresion, accesos, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.identificador = identificador
        self.parametro = parametro
        self.expresion = expresion
        self.accesos = accesos

    def getNodo(self):
        nodo = NodoAST('ASIGNACION STRUCT')
        nodo.agregar(self.identificador.getNodo())
        nodo.agregar('.')
        nodo.agregar(self.parametro)
        if self.accesos != None:
            for acceso in self.accesos:
                nodo.agregar('[')
                nodo.agregar(acceso.getNodo())
                nodo.agregar(']')
        nodo.agregar('=')
        nodo.agregar(self.expresion.getNodo())
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):

        identificador = self.identificador.interpretar(arbol, tablaSimbolo)
        valStruct = arbol.getStruct(self.identificador.tipoStruct)
        if isinstance(identificador, Error):
            return identificador
        if self.identificador.tipo != TipoDato.STRUCT:
            return Error("Error Semantico", "Variable no es struct", self.linea, self.columna)

        for param in identificador:

            if param.getIdentificador() == self.parametro:
                if self.accesos != None:
                    if param.tipo != TipoDato.ARREGLO:
                        return Error("Error Semantico", "La variable debe ser de tipo arreglo", self.linea, self.columna)
                    variable = param
                    for acceso in self.accesos:
                        val = acceso.interpretar(arbol, tablaSimbolo)
                        if isinstance(val, Error):
                            return val
                        if acceso.tipo != TipoDato.ENTERO:
                            return Error("Error Semantico", "El tipo de dato debe ser entero", self.linea, self.columna)
                        try:
                            variable = variable.getValor()[str(val)]
                        except:
                            return Error("Error Semantico", "No se encontro el acceso", self.linea, self.columna)
                    valor = self.expresion.interpretar(arbol, tablaSimbolo)

                    if isinstance(valor, Error):
                        return valor
                    variable.tipo = self.expresion.tipo
                    variable.tipoStruct = self.expresion.tipoStruct
                    variable.mutable = self.expresion.mutable
                    variable.setValor(valor)
                    if not arbol.actualizarTabla(param.getIdentificador(), valor, self.linea, tablaSimbolo.getNombre(), self.columna):
                        nuevoSim = ReporteTabla(param.getIdentificador(), valor, 'VariableStruct', str(
                            self.expresion.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
                        arbol.getSimbolos().append(nuevoSim)
                    return None
                else:
                    self.tipo = param.getTipo()
                    val = self.expresion.interpretar(arbol, tablaSimbolo)
                    if isinstance(val, Error):
                        return val
                    if self.noNulo(valStruct, self.parametro):
                        if param.getTipo() != self.expresion.tipo:
                            return Error("Error Semantico", "tipo de dato diferente", self.linea, self.columna)
                    param.setTipo(self.expresion.tipo)
                    param.tipoStruct = self.expresion.tipoStruct
                    param.mutable = self.expresion.mutable
                    param.setValor(val)
                    if not arbol.actualizarTabla(param.getIdentificador(), val, self.linea, tablaSimbolo.getNombre(), self.columna):
                        nuevoSim = ReporteTabla(param.getIdentificador(), val, 'VariableStruct', str(
                            self.expresion.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
                        arbol.getSimbolos().append(nuevoSim)
                    return None
        return Error("Error Semantico", "No existe este parametro dentro del struct", self.linea, self.columna)

    def noNulo(self, struct, parametro):
        if struct != None:
            for param in struct.parametros:
                if param["identificador"] == parametro:
                    if param["tipato"] == None:
                        return False
                    return True
        else:
            return False
