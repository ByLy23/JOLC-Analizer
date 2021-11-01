from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.instrucciones.AsigDeclaracion.Declaracion import Declaracion
from controlador.analizador.simbolos.SimboloC3D import SimboloC3D
from controlador.analizador.simbolos.TablaSimbolosC3D import TablaSimbolosC3D
from controlador.reportes.ReporteTabla import ReporteTabla
from controlador.analizador.simbolos.Simbolo import Simbolo
from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondFor(Instruccion):
    def __init__(self, ide, tipoRango, instrucciones, linea, columna):
        super().__init__(TipoDato.CADENA, linea, columna)
        self.ide = ide
        self.tipoRango = tipoRango
        self.instrucciones = instrucciones

    def traducir(self, arbol, tablaSimbolo):
        codigo = ""
        tempControl = arbol.newTemp()
        lControl = arbol.newLabel()

        lFalso = arbol.newLabel()
        lSalida = arbol.newLabel()
        nuevaTabla = TablaSimbolosC3D(tablaSimbolo)
        nuevaTabla.setNombre('While')
        arbol.tamReturn += tablaSimbolo.tamanio
        codigo += arbol.masStackV(tablaSimbolo.tamanio)
        dec = Declaracion(TipoDato.ENTERO, self.linea,
                          self.columna, self.ide, None, self.tipoStruct)
        nuevaDec = dec.traducir(arbol, nuevaTabla)
        if isinstance(nuevaDec, Error):
            return nuevaDec
        if self.tipoRango["exp2"] != None:
            val1 = self.tipoRango["exp1"].traducir(arbol, nuevaTabla)
            if isinstance(val1, Error):
                return val1
            val2 = self.tipoRango["exp2"].traducir(arbol, nuevaTabla)
            if isinstance(val2, Error):
                return val2
            if self.tipoRango["exp1"].tipo != TipoDato.ENTERO or self.tipoRango["exp2"].tipo != TipoDato.ENTERO:
                return Error("Error Semantico", "Rango no entero", self.linea, self.columna)
            codigo += val1["codigo"]
            codigo += val2["codigo"]
            codigo += arbol.assigTemp1(
                tempControl["temporal"], val1["temporal"])
            codigo += arbol.getLabel(lControl)
            codigo += arbol.getCond2(tempControl["temporal"],
                                     ">", val2["temporal"], lSalida)
            codigo += arbol.assigStackN("P", tempControl["temporal"])
            codigo += arbol.goto(lFalso)
            codigo += arbol.getLabel(lFalso)
            # Instrucciones
            tip = TipoDato.ENTERO
            aux = ""
            for i in self.instrucciones:
                i.eSetSalida(lSalida)
                i.eSetContinua(lControl)
                i.eSetReturn(self.eReturn())
                i.eSetTemporal(self.eTemporal())
                a = i.traducir(arbol, nuevaTabla)
                if isinstance(a, Error):
                    arbol.getErrores().append(a)
                    arbol.actualizaConsola(a.retornaError())
                    continue
                if 'tipo' in a:
                    tip = a["tipo"]
                    self.tipoStruct = i.tipoStruct
                    self.mutable = i.mutable
                aux += a["codigo"]
            codigo += aux
            codigo += arbol.assigTemp2(tempControl["temporal"],
                                       tempControl["temporal"], "+", "1.0")
            codigo += arbol.goto(lControl)
        # codigo = ""
        # lFalso = arbol.newTemp()
        # lVerdadero = arbol.newTemp()
        # lControl = arbol.newTemp()
        # if self.tipoRango["exp2"] != None:
        #     val1 = self.tipoRango["exp1"].traducir(arbol, tablaSimbolo)
        #     if isinstance(val1, Error):
        #         return val1
        #     val2 = self.tipoRango["exp2"].traducir(arbol, tablaSimbolo)
        #     if isinstance(val2, Error):
        #         return val2
        #     if self.tipoRango["exp1"].tipo != TipoDato.ENTERO or self.tipoRango["exp2"].tipo != TipoDato.ENTERO:
        #         return Error("Error Semantico", "Rango no entero", self.linea, self.columna)
        #     # print(val1, val2)
        #     nuevaTabla = TablaSimbolosC3D(tablaSimbolo)
        #     nuevaTabla.setNombre('For')
        #     arbol.tamReturn += tablaSimbolo.tamanio
        #     codigo += arbol.masStackV(tablaSimbolo.tamanio)
        #     # for i in range(val1, val2+1):
        #     #     otraTabla = TablaSimbolos(tablaSimbolo)
        #     #     otraTabla.setNombre('For')
        #     #     if otraTabla.setVariable(Simbolo(self.ide, TipoDato.ENTERO, i)) != 'La variable existe':
        #     #         variable = otraTabla.getVariable(self.ide)
        #     #         variable.setValor(i)
        #     tip = TipoDato.ENTERO
        #     aux = ""
        #     for i in self.instrucciones:
        #         i.eSetSalida(lFalso)
        #         i.eSetContinua(lControl)
        #         i.eSetReturn(self.eReturn())
        #         i.eSetTemporal(self.eTemporal())
        #         a = i.traducir(arbol, nuevaTabla)
        #         if isinstance(a, Error):
        #             arbol.getErrores().append(a)
        #             arbol.actualizaConsola(a.retornaError())
        #             continue
        #         if 'tipo' in a:
        #             tip = a["tipo"]
        #             self.tipoStruct = i.tipoStruct
        #             self.mutable = i.mutable
        #         aux += a["codigo"]
        #         print(aux)
        #     codigo += aux
        codigo += arbol.getLabel(lSalida)
        arbol.tamReturn -= tablaSimbolo.tamanio
        codigo += arbol.menosStackV(tablaSimbolo.tamanio)
        return {'temporal': '', 'codigo': codigo, 'tipo': tip}

    def getNodo(self):
        nodo = NodoAST('CICLO FOR')
        nodo.agregar('for')
        nodo.agregar(self.ide)
        nodo.agregar('in')
        if self.tipoRango["exp2"] != None:
            nodo.agregarAST(self.tipoRango["exp1"].getNodo())
            nodo.agregar(':')
            nodo.agregarAST(self.tipoRango["exp2"].getNodo())
        else:
            nodo.agregarAST(self.tipoRango["exp1"].getNodo())
        for inst in self.instrucciones:
            nodo.agregarAST(inst.getNodo())
        nodo.agregar('end')
        nodo.agregar(';')
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        if self.tipoRango["exp2"] != None:
            val1 = self.tipoRango["exp1"].interpretar(arbol, tablaSimbolo)
            if isinstance(val1, Error):
                return val1
            val2 = self.tipoRango["exp2"].interpretar(arbol, tablaSimbolo)
            if isinstance(val2, Error):
                return val2
            if self.tipoRango["exp1"].tipo != TipoDato.ENTERO or self.tipoRango["exp2"].tipo != TipoDato.ENTERO:
                return Error("Error Semantico", "Rango no entero", self.linea, self.columna)
            for i in range(val1, val2+1):
                otraTabla = TablaSimbolos(tablaSimbolo)
                otraTabla.setNombre('For')
                if otraTabla.setVariable(Simbolo(self.ide, TipoDato.ENTERO, i)) != 'La variable existe':
                    variable = otraTabla.getVariable(self.ide)
                    variable.setValor(i)

                if not arbol.actualizarTabla(self.ide, i, self.linea, 'ForDentro', self.columna):
                    nuevoSim = ReporteTabla(self.ide, i, 'ForDentro', str(
                        self.tipo), otraTabla.getNombre(), self.linea, self.columna)
                    arbol.getSimbolos().append(nuevoSim)
                for item in self.instrucciones:
                    res = item.interpretar(arbol, otraTabla)
                    if isinstance(res, Error):
                        arbol.getErrores().append(res)
                        arbol.actualizaConsola(res.retornaError())
                    if isinstance(res, Return):
                        return res
                    if res == 'ByLyContinue':
                        break
                    if res == 'ByLy23':
                        return

            # Dato con dos expresiones
        else:
            val1 = self.tipoRango["exp1"].interpretar(arbol, tablaSimbolo)
            if isinstance(val1, Error):
                return val1
            if self.tipoRango["exp1"].tipo == TipoDato.CADENA:
                for inst in val1:
                    otraTabla = TablaSimbolos(tablaSimbolo)
                    otraTabla.setNombre('For')
                    # TODO preguntar sobre el tipo de dato si es cadena o caracter
                    if otraTabla.setVariable(Simbolo(self.ide, TipoDato.CADENA, inst)) != 'La variable existe':
                        variable = otraTabla.getVariable(self.ide)
                        variable.setValor(inst)
                    if not arbol.actualizarTabla(self.ide, inst, self.linea, 'ForDentro', self.columna):
                        nuevoSim = ReporteTabla(self.ide, inst, 'ForDentro', str(
                            self.tipo), otraTabla.getNombre(), self.linea, self.columna)
                        arbol.getSimbolos().append(nuevoSim)
                    for item in self.instrucciones:
                        res = item.interpretar(arbol, otraTabla)
                        if isinstance(res, Error):
                            arbol.getErrores().append(res)
                            arbol.actualizaConsola(res.retornaError())
                        if isinstance(res, Return):
                            return res
                        if res == 'ByLyContinue':
                            break
                        if res == 'ByLy23':
                            return
            elif self.tipoRango["exp1"].tipo == TipoDato.ARREGLO:

                # TODO esto funciona con diccionario, revisar bien
                for clave, valor in val1.items():
                    otraTabla = TablaSimbolos(tablaSimbolo)
                    otraTabla.setNombre('For')
                    # TODO variable valor va a ser un simbolo
                    # print(valor.tipo, valor.getValor())
                    if otraTabla.setVariable(Simbolo(self.ide, valor.tipo, valor.getValor())) != 'La variable existe':
                        variable = otraTabla.getVariable(self.ide)
                        variable.setValor(valor.getValor())
                    if not arbol.actualizarTabla(self.ide, valor.getValor(), self.linea, 'ForDentro', self.columna):
                        nuevoSim = ReporteTabla(self.ide, valor.getValor(), 'ForDentro', str(
                            self.tipo), otraTabla.getNombre(), self.linea, self.columna)
                        arbol.getSimbolos().append(nuevoSim)
                    for item in self.instrucciones:
                        res = item.interpretar(arbol, otraTabla)
                        if isinstance(res, Error):
                            arbol.getErrores().append(res)
                            arbol.actualizaConsola(res.retornaError())
                        if isinstance(res, Return):
                            return res
                        if res == 'ByLyContinue':
                            break
                        if res == 'ByLy23':
                            return
            # Dato con una expresion
            else:
                return Error("Error Semantico", "Tipo de dato no admitido en For de una sola expresion", self.linea, self.columna)
        return None
