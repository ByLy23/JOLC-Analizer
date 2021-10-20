from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.SimboloC3D import SimboloC3D
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

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        if self.valor == None:  # valor Nothing
            if tablaSimbolo.getVariableEntorno(self.identificador) == None:
                tVar = arbol.newTemp()
                tStck = arbol.newTemp()
                codigo += arbol.assigTemp1(tVar["temporal"], "-50251313792.0")
                codigo += arbol.assigTemp2(tStck["temporal"],
                                           "P", "+", tablaSimbolo.getTamanio())
                codigo += arbol.assigStackN(tStck["temporal"],
                                            tVar["temporal"])
                simbolo = SimboloC3D(
                    self.tipo, self.identificador, tablaSimbolo.getTamanio(), True)
                simbolo.tipoStruct = self.struct
                simbolo.mutable = True
                tablaSimbolo.setVariable(simbolo)
            else:
                return Error("Error Compilacion", "{} no es compatible con {} ".format(self.valor.tipo, self.tipo), self.linea, self.columna)
            # if getVariable(self.identificador) Crea variable
            # t1=-50251313792.0 call me maybe xd
            #t2= P
            # stack[t2]=t1
            # P=P+1
            # # SIMBOLO (self, tipo, identificador, temporal, num, esConst):
            # simbolo = SimboloC3D(self.tipo,self.identificador,temporal,, None)
            # simbolo.tipoStruct = self.struct
            # simbolo.mutable = True

        else:
            val = self.valor.traducir(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            if self.valor.tipo != self.tipo:
                return Error("Error Compilacion", "{} no es compatible con {} ".format(self.valor.tipo, self.tipo), self.linea, self.columna)
            if self.valor.tipo == TipoDato.STRUCT:
                if self.valor.tipoStruct != self.struct:
                    return Error("Error Compilacion", "No es el mismo struct", self.linea, self.columna)
            codigo += val["codigo"]
            if tablaSimbolo.getVariableEntorno(self.identificador) == None:
                # if not cadena, struct o arreglo:
                if self.valor.tipo != TipoDato.CADENA and self.valor.tipo != TipoDato.STRUCT and self.valor.tipo != TipoDato.ARREGLO:
                    tVar = arbol.newTemp()
                    tStck = arbol.newTemp()
                    codigo += arbol.assigTemp1(tVar["temporal"],
                                               val["temporal"])
                    codigo += arbol.assigTemp2(tStck["temporal"],
                                               "P", "+", tablaSimbolo.getTamanio())
                    codigo += arbol.assigStackN(tStck["temporal"],
                                                tVar["temporal"])
                    nuevaVal = SimboloC3D(
                        self.tipo, self.identificador,  tablaSimbolo.getTamanio(), True)
                    nuevaVal.tipoStruct = self.valor.tipoStruct
                    nuevaVal.mutable = self.valor.mutable
                    tablaSimbolo.setVariable(nuevaVal)
                else:
                    tVar = arbol.newTemp()
                    tStck = arbol.newTemp()
                    codigo += arbol.assigTemp1(tVar["temporal"], val["heap"])
                    codigo += arbol.assigTemp2(tStck["temporal"],
                                               "P", "+", tablaSimbolo.getTamanio())
                    codigo += arbol.assigStackN(tStck["temporal"],
                                                tVar["temporal"])
                    nuevaVal = SimboloC3D(
                        self.tipo, self.identificador,  tablaSimbolo.getTamanio(), False)
                    nuevaVal.tipoStruct = self.valor.tipoStruct
                    nuevaVal.mutable = self.valor.mutable
                    tablaSimbolo.setVariable(nuevaVal)
                # else: guardar en heap y despues la referencia en stack
            else:
                return Error("Error Semantico", "La variable {} Existe actualmente".format(self.identificador), self.linea, self.columna)
        return {'codigo': codigo}

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
