from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.SimboloC3D import SimboloC3D
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

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        # TODO cambiar variable con if !=None
        var = tablaSimbolo.getVariable(self.identificador)
        variable = None
        cont = 0
        if var != None:
            variable = var["simbolo"]
            cont = var["entorno"]
        if variable == None:
            val = self.valor.traducir(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            print(val)
            if self.valor.tipo == TipoDato.STRUCT:
                if self.valor.tipoStruct != self.struct:
                    return Error("Error Compilacion", "No es el mismo struct", self.linea, self.columna)
            codigo += val["codigo"]
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
                    self.valor.tipo, self.identificador,  tablaSimbolo.getTamanio(), True)
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
                    self.valor.tipo, self.identificador,  tablaSimbolo.getTamanio(), False)
                nuevaVal.tipoStruct = self.valor.tipoStruct
                nuevaVal.mutable = self.valor.mutable
                tablaSimbolo.setVariable(nuevaVal)
            self.tipo = self.valor.tipo
            self.tipoStruct = self.valor.tipoStruct
            self.mutable = self.valor.mutable
            print(self.tipo)
            return {'codigo': codigo}

        # if not arbol.actualizarTabla(self.identificador, variable.valor, self.linea, tablaSimbolo.getNombre(), self.columna):
        #     nuevoSim = ReporteTabla(self.identificador, variable.valor, 'Variable', str(
        #         self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
        #     arbol.getSimbolos().append(nuevoSim)

        if variable.tipo != TipoDato.CADENA and variable.tipo != TipoDato.STRUCT and variable.tipo != TipoDato.ARREGLO:
            temp = arbol.newTemp()
            tempAcceso = arbol.newTemp()
            codigo += arbol.assigTemp2(tempAcceso["temporal"],
                                       "P", "-", cont)
            codigo += arbol.assigTemp2(tempAcceso["temporal"],
                                       tempAcceso["temporal"], "+", variable.getUbicacion())
            codigo += arbol.assigTemp1(temp["temporal"],
                                       tempAcceso["temporal"])
            # t1=stack[variable.temporal]
            # return {temporal:t1}
            val = self.valor.traducir(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            # if self.valor.tipo != self.tipo:
            #     return Error("Error Compilacion", "{} no es compatible con {} ".format(self.valor.tipo, self.tipo), self.linea, self.columna)
            if self.valor.tipo == TipoDato.STRUCT:
                if self.valor.tipoStruct != self.struct:
                    return Error("Error Compilacion", "No es el mismo struct", self.linea, self.columna)
            codigo += val["codigo"]
            tVar = arbol.newTemp()

            codigo += arbol.assigTemp1(tVar["temporal"],
                                       val["temporal"])
            codigo += arbol.assigStackN(temp["temporal"],
                                        tVar["temporal"])
            nuevaVal = SimboloC3D(
                self.tipo, self.identificador, variable.getUbicacion(), True)
            nuevaVal.tipoStruct = self.valor.tipoStruct
            nuevaVal.mutable = self.valor.mutable
            tablaSimbolo.setVariable(nuevaVal)
            return {'codigo': codigo}
        else:
            temp = arbol.newTemp()
            tempAcceso = arbol.newTemp()
            codigo += arbol.assigTemp2(tempAcceso["temporal"],
                                       "P", "-", cont)
            codigo += arbol.assigTemp2(tempAcceso["temporal"],
                                       tempAcceso["temporal"], "+", variable.getUbicacion())
            codigo += arbol.assigTemp1(temp["temporal"],
                                       tempAcceso["temporal"])
            # t1=stack[variable.temporal]
            # return {temporal:t1}
            val = self.valor.traducir(arbol, tablaSimbolo)
            if isinstance(val, Error):
                return val
            if self.valor.tipo != self.tipo:
                return Error("Error Compilacion", "{} no es compatible con {} ".format(self.valor.tipo, self.tipo), self.linea, self.columna)
            if self.valor.tipo == TipoDato.STRUCT:
                if self.valor.tipoStruct != self.struct:
                    return Error("Error Compilacion", "No es el mismo struct", self.linea, self.columna)
            codigo += val["codigo"]
            tVar = arbol.newTemp()
            codigo += arbol.assigTemp1(tVar["temporal"],
                                       val["heap"])
            codigo += arbol.assigStackN(temp["temporal"],
                                        tVar["temporal"])
            nuevaVal = SimboloC3D(
                self.tipo, self.identificador, variable.getUbicacion(), False)
            nuevaVal.tipoStruct = self.valor.tipoStruct
            nuevaVal.mutable = self.valor.mutable
            tablaSimbolo.setVariable(nuevaVal)
            self.tipo = variable.tipo
            self.tipoStruct = variable.tipoStruct
            self.mutable = variable.mutable
            return {'codigo': codigo}
            # t1=stack[variable.temporal] devuelve el apuntador del heap
            # return {heap:t1}

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

                    # if variable.tipo != TipoDato.NOTHING and variable.tipo != self.valor.tipo:
                    #     return Error("Error Semantico", "Variable {} con tipo de dato diferente".format(self.identificador), self.linea, self.columna)
                    # else:
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


# a=45;
# print(a);
