from optimizador.analizador.abstracto.Instruccion import Instruccion


class Encabezado(Instruccion):
    def __init__(self, lista, linea, columna):
        super().__init__(linea, columna)
        self.lista = lista

    def getInstruccion(self, arbol):
        imports = ""
        declas = "var "
        if "importaciones" in self.lista:
            for imp in self.lista["importaciones"]:
                imports += '"{}"'.format(imp)+"\n"

        if "declaraciones" in self.lista:
            for imp in self.lista["declaraciones"]:
                for dec in imp:
                    declas += '"{}"'.format(str(dec))[1:-1]+","
        declas = declas[0:-1]+" float64;\n"
        c = """package main;
import ({});\n
var stack [30000000] float64;
var heap [30000000] float64;
var P,H float64;\n""".format(imports)
        c += declas
        print(c, imports)
        return c

    def getNormal(self):
        imports = ""
        declas = "var "
        if "importaciones" in self.lista:
            for imp in self.lista["importaciones"]:
                imports += '"{}"'.format(imp)+","
        imports = imports[0:-1]
        if "declaraciones" in self.lista:
            for imp in self.lista["declaraciones"]:
                for dec in imp:
                    declas += '"{}"'.format(str(dec))[1:-1]+","
        declas = declas[0:-1]+" float64;\n"
        c = """package main;
import ({});\n
var stack [30000000] float64;
var heap [30000000] float64;
var P,H float64;\n""".format(imports)
        c += declas
        print(c, imports)
        return c
