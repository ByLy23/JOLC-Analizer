from controlador.analizador.abstracto.NodoAST import NodoAST
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion


class Continue(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)

    def getNodo(self):
        nodo = NodoAST('CONTINUE')
        nodo.agregar('continue')
        nodo.agregar(';')

        return nodo

    def traducir(self, arbol, tablaSimbolo):
        if self.eContinua() != None:
            codigo = ""
            codigo += arbol.menosStackV(tablaSimbolo.tamanio)
            codigo += arbol.goto(self.eContinua())

            return {'temporal': "", 'codigo': codigo}
        return Error("Error de Compilacion", "Sentencia fuera de ciclo", self.linea, self.columna)

    def interpretar(self, arbol, tablaSimbolo):
        return 'ByLyContinue'
