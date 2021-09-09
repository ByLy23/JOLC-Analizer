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
            for i in range(val1, val2):
                otraTabla = TablaSimbolos(tablaSimbolo)
                otraTabla.setNombre('For')
                if otraTabla.setVariable(Simbolo(self.ide, TipoDato.ENTERO, i)) != 'La variable existe':
                    variable = otraTabla.getVariable(self.ide)
                    variable.setValor(i)
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
                    if otraTabla.setVariable(Simbolo(self.ide, valor.tipo, valor.getValor())) != 'La variable existe':
                        variable = otraTabla.getVariable(self.ide)
                        variable.setValor(valor.getValor())
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
