from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class CondFor(Instruccion):
    def __init__(self, declaSignacion, condicion, actualizacion, instrucciones, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.declaSignacion = declaSignacion
        self.actualizacion = actualizacion
        self.condicion = condicion
        self.instrucciones = instrucciones

    def interpretar(self, arbol, tablaSimbolo):
        nuevaTabla = TablaSimbolos(tablaSimbolo)
        nuevaTabla.setNombre('For')
        declaAsig = self.declaSignacion.interpretar(arbol, nuevaTabla)
        if isinstance(declaAsig, Error):
            return declaAsig
        val = self.condicion.interpretar(arbol, nuevaTabla)
        if isinstance(val, Error):
            return val
        if self.condicion.tipo != TipoDato.BOOLEANO:
            return Error("Error Semantico", "Debe ser booleano", self.linea, self.columna)
        while self.condicion.interpretar(arbol, nuevaTabla):
            otraTabla = TablaSimbolos(nuevaTabla)
            otraTabla.setNombre('ForDentro')
            for i in range(0, len(self.instrucciones)):
                a = self.instrucciones[i].interpretar(arbol, otraTabla)
                if isinstance(a, Error):
                    arbol.getErrores().append(a)
                    arbol.actualizaConsola(a.retornaError())
                # if return, break, continue
                if isinstance(a, Return):
                    return a
                if a == 'ByLyContinue':
                    break
                if a == 'ByLy23':
                    return
            valActualizacion = self.actualizacion.interpretar(
                arbol, nuevaTabla)
            if isinstance(valActualizacion, Error):
                return valActualizacion
