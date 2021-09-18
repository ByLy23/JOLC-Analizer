from controlador.reportes.ReporteTabla import ReporteTabla
from re import L
from controlador.analizador.instrucciones.AsigDeclaracion.Asignacion import Asignacion
from controlador.analizador.instrucciones.transferencia.Break import Break
from controlador.analizador.simbolos.TablaSimbolos import TablaSimbolos
from controlador.analizador.instrucciones.transferencia.Return import Return
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.abstracto.Instruccion import Instruccion


class Funcion(Instruccion):
    def __init__(self, tipo, linea, columna, identificador, parametros, instrucciones):
        super().__init__(tipo, linea, columna)
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones

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
