from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Return(Instruccion):
    valor = None

    def __init__(self, linea, columna, expresion=None):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.expresion = expresion

    def traducir(self, arbol, tablaSimbolo):  # pendiente
        codigo = ""
        if self.expresion != None:
            self.expresion.eSetTemporal(self.eTemporal())
            self.valor = self.expresion.traducir(arbol, tablaSimbolo)
            codigo += self.valor["codigo"]
            self.tipo = self.expresion.tipo
            self.tipoStruct = self.expresion.tipoStruct
            self.mutable = self.expresion.mutable
            if self.expresion.tipo != TipoDato.CADENA and self.expresion.tipo != TipoDato.STRUCT and self.expresion.tipo != TipoDato.ARREGLO:
                codigo += arbol.assigStackN(self.eTemporal(),
                                            self.valor["temporal"])
                codigo += arbol.menosStackV(arbol.tamReturn)

                codigo += arbol.goto(self.eReturn())
            else:
                codigo += arbol.assigStackN(self.eTemporal(),
                                            self.valor["heap"])
                codigo += arbol.menosStackV(arbol.tamReturn)
                codigo += arbol.goto(self.eReturn())
        else:
            self.tipo = TipoDato.NOTHING
            codigo += arbol.assigStackN(self.eTemporal(), "-50251313792")
            codigo += arbol.goto(self.eReturn())
        return {'codigo': codigo, 'tipo': self.expresion.tipo}

    def getNodo(self):
        nodo = NodoAST('RETURN')
        nodo.agregar('return')
        if self.expresion != None:
            nodo.agregarAST(self.expresion.getNodo())
        return nodo

    def interpretar(self, arbol, tablaSimbolo):
        if self.expresion != None:
            self.valor = self.expresion.interpretar(arbol, tablaSimbolo)
            self.tipo = self.expresion.tipo
            self.tipoStruct = self.expresion.tipoStruct
            self.mutable = self.expresion.mutable
        return self
