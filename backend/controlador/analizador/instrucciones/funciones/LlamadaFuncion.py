from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.TablaSimbolosC3D import TablaSimbolosC3D
from controlador.reportes.ReporteTabla import ReporteTabla
from controlador.analizador.instrucciones.AsigDeclaracion.Asignacion import Asignacion
from controlador.analizador.simbolos.Simbolo import Simbolo
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

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        funcion = arbol.getFuncion(self.identificador)
        if funcion != None:
            # return Error("Error Semantico", "No se encontro la Funcion", self.linea, self.columna)
            if len(funcion.parametros) == len(self.parametros):
                nuevaTabla = TablaSimbolosC3D(tablaSimbolo)
                codigo += arbol.masStackV(tablaSimbolo.tamanio)
                iterador = 0
                nuevaTabla.masTamanio()
                varTemps = arbol.getTempNoUsados()
                nuevoTemp = arbol.newTemp()
                codigo += arbol.assigTemp1(nuevoTemp["temporal"], "P")
                for t in varTemps:
                    codigo += arbol.masStackV(1)
                    codigo += "stack[int({})] = {};\n".format(
                        nuevoTemp["temporal"], t)

                    codigo += arbol.assigTemp2(
                        nuevoTemp["temporal"], nuevoTemp["temporal"], "+", "1")

                nuevaTabla.getAnterior().setTamanio(
                    nuevaTabla.getAnterior().getTamanio()+len(varTemps))
                for nuevoVal in self.parametros:
                    val = nuevoVal.traducir(arbol, nuevaTabla)
                    if isinstance(val, Error):
                        return val
                    if isinstance(funcion.parametros[iterador]["tipato"], str):
                        # Se realiza como un struct
                        dec = Declaracion(TipoDato.STRUCT, funcion.linea,
                                          funcion.columna, funcion.parametros[iterador]["identificador"]+"50251", nuevoVal, funcion.parametros[iterador]["tipato"])

                        nuevaDec = dec.traducir(arbol, nuevaTabla)
                        if isinstance(nuevaDec, Error):
                            return nuevaDec

                        codigo += nuevaDec["codigo"]

                        var = nuevaTabla.getVariable(
                            funcion.parametros[iterador]["identificador"]+"50251")
                        if var != None:
                            # if var.tipo != nuevoVal.tipo:
                            #     return Error("Semantico", "Tipo de dato diferente", self.linea, self.columna)
                            # else:
                            var.mutable = nuevoVal.mutable
                            var.tipoStruct = nuevoVal.tipoStruct
                            var.setValor(val)
                            nuevaTabla.setNombre(funcion.identificador)
                        else:
                            return Error("Error Semantico", "Variable no existe", self.linea, self.columna)
                    else:

                        dec = Declaracion(nuevoVal.tipo, funcion.linea,
                                          funcion.columna, funcion.parametros[iterador]["identificador"]+"50251", nuevoVal, nuevoVal.tipoStruct)

                        nuevaDec = dec.traducir(arbol, nuevaTabla)
                        if isinstance(nuevaDec, Error):
                            return nuevaDec
                        codigo += nuevaDec["codigo"]
                        # var = nuevaTabla.getVariable(
                        #     funcion.parametros[iterador]["identificador"])
                        # if var != None:
                        #     # if var.tipo != nuevoVal.tipo:
                        #     #     return Error("Semantico", "Tipo de dato diferente", self.linea, self.columna)
                        #     # else:
                        #     var.setValor(val)
                        #     var.tipoStruct = nuevoVal.tipoStruct
                        #     nuevaTabla.setNombre(funcion.identificador)
                        # else:
                        #     return Error("Error Semantico", "Variable no existe", self.linea, self.columna)
                    # if not arbol.actualizarTabla(funcion.parametros[iterador]["identificador"], 'nothing', self.linea, nuevaTabla.getNombre(), self.columna):
                    #     nuevoSim = ReporteTabla(funcion.parametros[iterador]["identificador"], 'nothing', 'Parametro', str(
                    #         var.tipo), nuevaTabla.getNombre(), self.linea, self.columna)
                    #     arbol.getSimbolos().append(nuevoSim)
                    iterador = iterador+1

                # nuevoMet = funcion.traducir(arbol, nuevaTabla)

                # if isinstance(nuevoMet, Error):
                #     return nuevoMet
                # self.tipo = funcion.tipo
                # self.tipoStruct = funcion.tipoStruct
                # self.mutable = funcion.mutable
                # codigo += nuevoMet["codigo"]
                codigo += self.identificador+"();\n"
                aux2 = ""

                nuevaTabla.getAnterior().setTamanio(
                    nuevaTabla.getAnterior().getTamanio()-len(varTemps))
                for t in reversed(varTemps):
                    aux2 += arbol.menosStackV(1)
                    aux2 += "{} = stack[int({})];\n".format(t, "P")
                nuevoTemp = arbol.newTemp()
                codigo += arbol.assigTemp1(nuevoTemp["temporal"], "P")

                # TODO hacer un metodo que obtenga los temporales usados antes de que llamen una funcion
                # print(arbol.getTempNoUsados())
                tempRetorno = arbol.newTemp()
                codigo += arbol.getStack(tempRetorno["temporal"],
                                         nuevoTemp["temporal"])
                codigo += aux2
                codigo += arbol.menosStackV(tablaSimbolo.tamanio)
                # if not arbol.actualizarTabla(self.identificador, nuevoMet, self.linea, 'Funcion', self.columna):
                #     nuevoSim = ReporteTabla(self.identificador, nuevoMet, 'Funcion', str(
                #         self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
                #     arbol.getSimbolos().append(nuevoSim)
                self.tipo = funcion.tipo
                return {'heap': tempRetorno["temporal"], 'temporal': tempRetorno["temporal"], 'codigo': codigo}
            else:
                return Error("Error Semantico", "parametros no coincidientes", self.linea, self.columna)

    def getNodo(self):
        nodo = NodoAST('LLAMADA FUNCION')
        nodo.agregar(self.identificador)
        nodo.agregar('(')
        for param in self.parametros:
            nodo.agregarAST(param.getNodo())
            nodo.agregar(',')
        nodo.agregar(')')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        funcion = arbol.getFuncion(self.identificador)
        if funcion != None:
            # return Error("Error Semantico", "No se encontro la Funcion", self.linea, self.columna)
            if len(funcion.parametros) == len(self.parametros):
                nuevaTabla = TablaSimbolos(tablaSimbolo)
                iterador = 0
                for nuevoVal in self.parametros:
                    val = nuevoVal.interpretar(arbol, tablaSimbolo)
                    if isinstance(val, Error):
                        return val
                    if isinstance(funcion.parametros[iterador]["tipato"], str):
                        # Se realiza como un struct
                        dec = Declaracion(TipoDato.STRUCT, funcion.linea,
                                          funcion.columna, funcion.parametros[iterador]["identificador"], nuevoVal, funcion.parametros[iterador]["tipato"])
                        nuevaDec = dec.interpretar(arbol, nuevaTabla)
                        if isinstance(nuevaDec, Error):
                            return nuevaDec
                        var = nuevaTabla.getVariable(
                            funcion.parametros[iterador]["identificador"])
                        if var != None:
                            # if var.tipo != nuevoVal.tipo:
                            #     return Error("Semantico", "Tipo de dato diferente", self.linea, self.columna)
                            # else:
                            var.mutable = nuevoVal.mutable
                            var.tipoStruct = nuevoVal.tipoStruct
                            var.setValor(val)
                            nuevaTabla.setNombre(funcion.identificador)
                        else:
                            return Error("Error Semantico", "Variable no existe", self.linea, self.columna)
                    else:

                        dec = Declaracion(nuevoVal.tipo, funcion.linea,
                                          funcion.columna, funcion.parametros[iterador]["identificador"], nuevoVal, nuevoVal.tipoStruct)
                        nuevaDec = dec.interpretar(arbol, nuevaTabla)
                        if isinstance(nuevaDec, Error):
                            return nuevaDec
                        var = nuevaTabla.getVariable(
                            funcion.parametros[iterador]["identificador"])
                        if var != None:
                            # if var.tipo != nuevoVal.tipo:
                            #     return Error("Semantico", "Tipo de dato diferente", self.linea, self.columna)
                            # else:
                            var.setValor(val)
                            var.tipoStruct = nuevoVal.tipoStruct
                            nuevaTabla.setNombre(funcion.identificador)
                        else:
                            return Error("Error Semantico", "Variable no existe", self.linea, self.columna)
                    if not arbol.actualizarTabla(funcion.parametros[iterador]["identificador"], 'nothing', self.linea, nuevaTabla.getNombre(), self.columna):
                        nuevoSim = ReporteTabla(funcion.parametros[iterador]["identificador"], 'nothing', 'Parametro', str(
                            var.tipo), nuevaTabla.getNombre(), self.linea, self.columna)
                        arbol.getSimbolos().append(nuevoSim)
                    iterador = iterador+1

                nuevoMet = funcion.interpretar(arbol, nuevaTabla)
                if isinstance(nuevoMet, Error):
                    return nuevoMet
                self.tipo = funcion.tipo
                self.tipoStruct = funcion.tipoStruct
                self.mutable = funcion.mutable

                # if not arbol.actualizarTabla(self.identificador, nuevoMet, self.linea, 'Funcion', self.columna):
                #     nuevoSim = ReporteTabla(self.identificador, nuevoMet, 'Funcion', str(
                #         self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
                #     arbol.getSimbolos().append(nuevoSim)
                return nuevoMet
            else:
                return Error("Error Semantico", "parametros no coincidientes", self.linea, self.columna)
        # SE VERIFICA SI ES STRUCT
        listaStruct = []
        valStruct = arbol.getStruct(self.identificador)
        if valStruct == None:
            return Error("Error Semantico", "La variable no es funcion ni estruct", self.linea, self.columna)

        self.tipoStruct = self.identificador
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
                if nuevoVal.tipo == TipoDato.STRUCT:
                    if valStruct.parametros[iterador]["tipoStruct"] != nuevoVal.tipoStruct:
                        return Error("Error Semantico", "Tipo de Struct diferente", self.linea, self.columna)
            # se agrega el simbolo de cda parametro del struct
            simbolo = Simbolo(
                valStruct.parametros[iterador]["identificador"], nuevoVal.tipo, val)
            simbolo.tipoStruct = nuevoVal.tipoStruct
            simbolo.mutable = nuevoVal.mutable
            listaStruct.append(simbolo)
            # if not arbol.actualizarTabla(valStruct.parametros[iterador]["identificador"], val, self.linea, 'Struct', self.columna):
            #     nuevoSim = ReporteTabla(self.identificador, val, 'Struct', str(
            #         self.tipo), tablaSimbolo.getNombre(), self.linea, self.columna)
            #     arbol.getSimbolos().append(nuevoSim)
            iterador = iterador+1
        self.tipo = TipoDato.STRUCT
        self.tipoStruct = self.identificador
        self.mutable = True

        return listaStruct
