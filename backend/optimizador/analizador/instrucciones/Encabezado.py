from optimizador.analizador.abstracto.Instruccion import Instruccion


class Encabezado(Instruccion):
    def __init__(self, lista, linea, columna):
        super().__init__(linea, columna)
        self.lista = lista

    def getInstruccion(self, arbol):
        imports = ""
        print(len(self.lista))
        if len(self.lista) == 2:
            for i in self.lista[2]:
                imports += i+","
            imports = imports[0, -1]
        c = """package main;
        import ({});\n
        var stack [30000000] float64;
        var heap [30000000] float64;
        var P,H float64;""".format(imports)
        print(c, imports)
