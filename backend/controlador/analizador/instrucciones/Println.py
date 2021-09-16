from controlador.analizador.instrucciones.struct.AccesoStruct import AccesoStruct
from ..abstracto.Instruccion import Instruccion
from ..excepciones.Error import Error
from ..simbolos.Arbol import Arbol
from ..simbolos.Tipo import TipoDato


class Println(Instruccion):
    def __init__(self, linea, columna, expresion=""):
        super().__init__(TipoDato.CADENA, linea, columna)
        self.expresion = expresion
        self.linea = linea
        self.columna = columna

    def interpretar(self, arbol, tablaSimbolo):
        for valor in self.expresion:
            variable = valor.interpretar(arbol, tablaSimbolo)
            if isinstance(variable, Error):
                return variable
            if variable == None:
                err = Error(
                    "Error Semantico", "No existe ningun valor que mostrar", self.linea, self.columna)
                arbol.getErrores().append(err)
                arbol.actualizaConsola(err.retornaError()+"\n")
            if valor.tipo == TipoDato.ARREGLO:
                arbol.actualizaConsola(self.impresion(variable).replace(
                    '(,', '("",').replace(',,', ',"",').replace(',)', ',"")'))
            elif valor.tipo == TipoDato.STRUCT:
                if isinstance(valor, AccesoStruct):
                    arbol.actualizaConsola(
                        valor.parametro+self.impresionStruct(variable).replace('(,', '("",').replace(',,', ',"",').replace(',)', ',"")'))
                else:
                    arbol.actualizaConsola(
                        valor.identificador+self.impresionStruct(variable).replace('(,', '("",').replace(',,', ',"",').replace(',)', ',"")'))
            else:
                arbol.actualizaConsola(str(variable).replace(
                    '(,', '("",').replace(',,', ',"",').replace(',)', ',"")'))
        arbol.actualizaConsola("\n")

    def impresionStruct(self, valor):
        dato = ""
        dato = dato+"("
        for val in valor:
            if val.tipo == TipoDato.ARREGLO:
                dato = dato+self.impresion(val.getValor())+","
            elif val.tipo == TipoDato.STRUCT:
                dato = dato+val.tipoStruct + \
                    self.impresionStruct(val.getValor())+","
            else:
                dato = dato+str(val.getValor())+","
        dato = dato[:-1]+")"
        return dato

    def impresion(self, valor):
        dato = ""
        dato = dato+"["
        for val in valor.values():
            if val.tipo == TipoDato.ARREGLO:
                dato = dato+self.impresion(val.getValor())+","
            elif val.tipo == TipoDato.STRUCT:
                dato = dato+val.tipoStruct + \
                    self.impresionStruct(val.getValor())+","
            else:
                dato = dato+str(val.getValor())+","
        dato = dato[:-1]+"]"
        return dato
