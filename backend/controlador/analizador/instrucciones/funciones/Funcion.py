from controlador.analizador.instrucciones.AsigDeclaracion.Declaracion import Declaracion
from controlador.analizador.simbolos.TablaSimbolosC3D import TablaSimbolosC3D
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.reportes.ReporteTabla import ReporteTabla
from controlador.analizador.instrucciones.AsigDeclaracion.Asignacion import Asignacion
from controlador.analizador.instrucciones.transferencia.Break import Break
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.abstracto.Instruccion import Instruccion


class Funcion(Instruccion):
    def __init__(self, tipo, linea, columna, identificador, parametros, instrucciones):
        super().__init__(tipo, linea, columna)
        if tipo == TipoDato.NOTHING:
            self.tipo = TipoDato.ENTERO
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        aux = ""
        lSalida = arbol.newLabel()
        tablaSimbolo.masTamanio()
        codigo += "func " + self.identificador+"() {\n"
        nRetorno = arbol.newTemp()
        codigo += arbol.assigTemp1(nRetorno["temporal"], "P")
        for nuevoVal in self.parametros:
            if isinstance(nuevoVal["tipato"], str):
                # Se realiza como un struct
                tmpsNoUsados = arbol.getTempNoUsados()
                dec = Declaracion(TipoDato.STRUCT, self.linea,
                                  self.columna, nuevoVal["identificador"], None, nuevoVal["tipato"])
                nuevaDec = dec.traducir(arbol, tablaSimbolo)
                if isinstance(nuevaDec, Error):
                    return nuevaDec
                arbol.setTempNoUsados(tmpsNoUsados)
                # codigo += nuevaDec["codigo"]
            else:
                tmpsNoUsados = arbol.getTempNoUsados()
                dec = Declaracion(nuevoVal["tipato"], self.linea,
                                  self.columna, nuevoVal["identificador"], None, self.tipoStruct)
                nuevaDec = dec.traducir(arbol, tablaSimbolo)
                if isinstance(nuevaDec, Error):
                    return nuevaDec
                arbol.setTempNoUsados(tmpsNoUsados)

                # codigo += nuevaDec["codigo"]
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
        for inst in self.instrucciones:
            inst.eSetReturn(lSalida)
            inst.eSetTemporal(nRetorno["temporal"])
            valor = inst.traducir(arbol, tablaSimbolo)
            if isinstance(valor, Error):
                arbol.getErrores().append(valor)
                arbol.actualizaConsola(valor.retornaError())
                continue
            if 'tipo' in valor:
                self.tipo = valor["tipo"]
            aux += valor["codigo"]

            self.tipoStruct = inst.tipoStruct
            self.mutable = inst.mutable
        codigo += aux
        codigo += arbol.goto(lSalida)
        codigo += arbol.getLabel(lSalida)
        codigo += "return;\n}\n"
        arbol.tamReturn = 0
        print(self.tipo)
        return {'codigo': codigo}

    def getNodo(self):
        nodo = NodoAST('FUNCION')
        nodo.agregar('function')
        nodo.agregar(self.identificador)
        nodo.agregar('(')
        for param in self.parametros:
            if param["tipato"] != None:
                nodo.agregar(param["identificador"])
                nodo.agregar(':')
                nodo.agregar(':')
                nodo.agregar(param["tipato"])
            else:
                nodo.agregar(param["identificador"])
            nodo.agregar(',')
        nodo.agregar(')')
        for inst in self.instrucciones:
            nodo.agregarAST(inst.getNodo())
        nodo.agregar('end')
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        nuevaTabla = TablaSimbolos(tablaSimbolo)
        nuevaTabla.setNombre('Funcion')
        for inst in self.instrucciones:
            valor = inst.interpretar(arbol, nuevaTabla)
            if isinstance(valor, Error):
                arbol.getErrores().append(valor)
                arbol.actualizaConsola(valor.retornaError())
            if valor == 'ByLy23':
                error = Error("Error Semantico",
                              "Break fuera de ciclo", inst.linea, inst.columna)
                arbol.getErrores().append(error)
                arbol.actualizaConsola(error.retornaError())
            if isinstance(valor, Return):
                self.tipo = valor.tipo
                self.tipoStruct = valor.tipoStruct
                self.mutable = valor.mutable
                return valor.valor

        return None
        # for item in self.instrucciones:
        #     val = item.interpretar(arbol, tablaSimbolo)
        #     if isinstance(val, Error):
        #         return val
        #     if isinstance(val, Return):
        #         if(val.valor != None):
        #             if self.tipo == val.tipo:
        #                 return val.valor
        #             else:
        #                 return Error("Error Semantico", "Tipo de datos diferentes", self.linea, self.columna)
        #         else:
        #             return Error('Error Semantico', "La funcion debe devolver un valor", self.linea, self.columna)
