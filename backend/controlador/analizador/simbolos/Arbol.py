from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.reportes.ReporteTabla import ReporteTabla


class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.consola = ""
        self.funciones = []
        self.tablaGlobal = None
        self.errores = []
        self.listaSimbolos = []
        self.structs = []
        self.listaTemporales = []
        self.listaImports = ["\"fmt\""]
        # SEGUNDA FASE
        self.t = 0
        self.l = 0
    # gets

    def getStructs(self):
        return self.structs

    def getStruct(self, identificador):
        for f in self.structs:
            if identificador == f.identificador:
                if not self.actualizarTabla(f.identificador, '', f.linea, 'Global', f.columna):
                    nuevoSimbolo = ReporteTabla(
                        f.identificador, '', 'StructCreacion', f.tipo, 'Global', f.linea, f.columna)
                    self.listaSimbolos.append(nuevoSimbolo)
                return f
        return None

    def actualizarTabla(self, ide, valor, linea, entorno, columna):
        for elemento in self.listaSimbolos:
            if str(elemento.getIdentificador()) == str(ide) and str(elemento.getEntorno()) == str(entorno):
                elemento.setValor(valor)
                elemento.setLinea(linea)
                elemento.setColumna(columna)
                return True
        return False

    def buscarTipo(self, identificador):
        for elemento in self.listaSimbolos:
            if str(elemento.getIdentificador()) == identificador:
                return str(elemento.getForma())
        return 'as'

    def getFuncion(self, identificador):
        for f in self.funciones:
            if identificador == f.identificador:
                if not self.actualizarTabla(f.identificador, '', f.linea, 'Global', f.columna):
                    # TODO CAMBIAR TIPO DE DATO XD
                    nuevoSimbolo = ReporteTabla(f.identificador, '', 'FuncionCreacion', str(
                        f.tipo), 'Global', f.linea, f.columna)
                    self.listaSimbolos.append(nuevoSimbolo)
                return f
        return None

    def getSimbolos(self):
        return self.listaSimbolos

    def getErrores(self):
        return self.errores

    def getFunciones(self):
        return self.funciones

    def getInstrucciones(self):
        return self.instrucciones

    def getConsola(self):
        return self.consola

    def getGlobal(self):
        return self.tablaGlobal

    # sets
    def setFunciones(self, funciones):
        self.funciones = funciones

    def setErrores(self, errores):
        self.errores = errores

    def setImports(self, impor):
        self.listaImports.append(impor)

    def getImports(self):
        im = ""
        for i in self.listaImports:
            im += i+"\n"
        return im

    def setInstrucciones(self, instruccion):
        self.instrucciones = instruccion

    def setConsola(self, consola):
        self.consola = consola

    def setGlobal(self, tablaGlobal):
        self.tablaGlobal = tablaGlobal

    # actualizarConsola
    def actualizaConsola(self, actualizar):
        self.consola = "{}{}".format(self.consola, str(actualizar))

    def actualizarTabla(self, identificadr, valor, linea, entorno, columna):
        for item in self.listaSimbolos:
            if item.getIdentificador() == identificadr:
                item.setValor(valor)
                item.setLinea(linea)
                item.setEntorno(entorno)
                item.setColumna(columna)
                return True
        return False

    # SEGUNDA FASE

    def masStack(self, n):
        return "P = P + {};\n".format(n)

    def menosStack(self, n):
        return "P = P - {};\n".format(n)

    def masHeap(self, n):
        return "H = H + {};\n".format(n)

    def menosHeap(self, n):
        return "H = H - {};\n".format(n)

    def assigHeapH(self, n):
        return "heap"

    def nuevoTemp(self, temp):
        resultado = {'temporal': temp, 'codigo': ""}
        return resultado

    def newTemp(self, codigo=None):
        resultado = None
        if codigo == None:
            resultado = {'temporal': 't{}'.format(str(self.t)), 'codigo': ''}
        else:
            resultado = {'temporal': 't{}'.format(
                str(self.t)), 'codigo': codigo}
        self.listaTemporales.append('t{}'.format(str(self.t)))
        self.t += 1
        return resultado

    def assigTemp1(self, tempAsig, tempOperacion):
        return '{} = {};\n'.format(tempAsig, tempOperacion)

    def assigTemp2(self, tempAsig, tempOperacion1, operador, tempOperacion2):
        return '{} = {} {} {};\n'.format(tempAsig, tempOperacion1, operador, tempOperacion2)

    def assigTempMod(self, tempAsig, tempOperacion1, tempOperacion2):
        return '{} = math.Mod({},{});\n'.format(tempAsig, tempOperacion1, tempOperacion2)

    def newLabel(self):
        resultado = 'L{}'.format(str(self.l))
        self.l += 1
        return resultado

    def goto(self, l):
        return 'goto {};\n'.format(l)

    def getLabel(self, l):
        return '{}:\n'.format(l)

    def getCond1(self, temp, label):
        return 'if ('+temp+') {goto '+label+'};\n'

    def getCond2(self, c1, op, c2, label):
        return 'if ('+c1+' '+op+' '+c2+') {goto '+label+'};\n'

    def imprimir(self, temp):
        return 'fmt.Printf({});\n'.format(temp)
