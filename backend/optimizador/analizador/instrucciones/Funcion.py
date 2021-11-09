from optimizador.analizador.abstracto.Instruccion import Instruccion


class Funcion(Instruccion):
    def __init__(self, ide, instrucciones, linea, columna):
        super().__init__(linea, columna)
        self.ide = ide
        self.instrucciones = instrucciones

    def getInstruccion(self, arbol):
        # print(self.instrucciones)
        prueba = []
        codigo = ""
        for ins in self.instrucciones:
            prueba = ins.getInstruccion(arbol)
            codigo += prueba
            # print(prueba)
        return 'func '+self.ide+'(){\n'+codigo+'\n}\n'

    def getNormal(self):
        return 'func '+self.ide+'(){\n'+self.instrucciones+'\n}'
