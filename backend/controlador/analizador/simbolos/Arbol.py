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
        self.listaImports = []
        self.tempNoUsados = []
        # SEGUNDA FASE
        self.t = 0
        self.l = 0
        self.tamReturn = 0
    # gets

    def getStructs(self):
        return self.structs

    def getTempNoUsados(self):
        return self.tempNoUsados.copy()

    def setTempNoUsados(self, temp):
        self.tempNoUsados = temp

    def agregaTemp(self, temp):
        flag = True
        for t in self.tempNoUsados:
            if t == temp:
                flag = False
                break
        if flag:
            self.tempNoUsados.append(temp)

    def eliminaTemp(self, temp):
        for t in self.tempNoUsados:
            if t == temp:
                self.tempNoUsados.remove(temp)

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
        for i in self.listaImports:
            if i == impor:
                return
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

    def masStack(self):
        return "P = P + 1;\n"

    def menosStack(self):
        return "P = P - 1;\n"

    def masStackV(self, n):
        self.eliminaTemp(n)
        return "P = P + {};\n".format(n)

    def menosStackV(self, n):
        self.eliminaTemp(n)
        return "P = P - {};\n".format(n)

    def masHeap(self):
        return "H = H + 1;\n"

    def menosHeap(self):
        return "H = H - 1;\n"

    def assigHeapH(self, n):
        self.eliminaTemp(n)
        return "heap[int(H)] = {};\n".format(n)

    def assigHeap2(self, h, n):
        self.eliminaTemp(n)
        return "heap[int({})] = {};\n".format(h, n)

    def assigStackN(self, h, n):
        self.eliminaTemp(n)
        return "stack[int({})] = {};\n".format(h, n)

    def getHeap(self, temp, h):
        self.agregaTemp(temp)
        self.eliminaTemp(h)
        return "{} = heap[int({})];\n".format(temp, h)

    def getStack(self, temp, h):
        self.agregaTemp(temp)
        self.eliminaTemp(h)
        return "{} = stack[int({})];\n".format(temp, h)

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
        self.eliminaTemp(tempOperacion)
        self.agregaTemp(tempAsig)
        return '{} = {};\n'.format(tempAsig, tempOperacion)

    def assigTemp2(self, tempAsig, tempOperacion1, operador, tempOperacion2):
        self.eliminaTemp(tempOperacion1)
        self.eliminaTemp(tempOperacion2)
        self.agregaTemp(tempAsig)
        return '{} = {} {} {};\n'.format(tempAsig, tempOperacion1, operador, tempOperacion2)

    def assigTempMod(self, tempAsig, tempOperacion1, tempOperacion2):
        self.eliminaTemp(tempOperacion1)
        self.eliminaTemp(tempOperacion2)
        self.agregaTemp(tempAsig)
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
        return 'if ('+temp+') {goto '+label+';}\n'

    def getCond2(self, c1, op, c2, label):
        return 'if ('+c1+' '+op+' '+c2+') {goto '+label+';}\n'

    def imprimir(self, temp):
        return 'fmt.Printf({});\n'.format(temp)

    def guardarStr(self, cadena):
        codigo = ""
        temp = self.newTemp()
        codigo += self.assigTemp1(temp["temporal"], 'H')
        for i in cadena:
            codigo += self.assigHeapH(ord(i))
            codigo += self.masHeap()
        codigo += self.assigHeapH("-1")
        codigo += self.masHeap()
        return {'heap': temp["temporal"], 'codigo': codigo}

    def potenciaCadena(self, cadena, cantidad):
        temp = self.newTemp()
        codigo = ""
        tempo = self.newTemp()
        Ltemp = self.newTemp()
        loop = self.newLabel()
        lSalida = self.newLabel()
        lControl = self.newLabel()
        lSal1 = self.newLabel()
        tempControl = self.newTemp()
        codigo += self.assigTemp1(temp["temporal"], 'H')
        codigo += self.assigTemp1(tempo["temporal"], cadena)
        codigo += self.assigTemp1(tempControl["temporal"], cantidad)
        codigo += self.getLabel(lControl)
        codigo += self.getCond2(tempControl["temporal"], "<=", "1.0", lSalida)
        codigo += self.getLabel(loop)
        codigo += self.getHeap(Ltemp["temporal"], tempo["temporal"])
        codigo += self.getCond2(Ltemp["temporal"], "==", "-1.0", lSal1)
        codigo += self.assigHeapH(Ltemp["temporal"])
        codigo += self.masHeap()
        codigo += self.assigTemp2(tempo["temporal"],
                                  tempo["temporal"], "+", "1")
        codigo += self.goto(loop)
        codigo += self.getLabel(lSal1)
        codigo += self.assigTemp2(tempControl["temporal"],
                                  tempControl["temporal"], "-", "1.0")
        codigo += self.goto(lControl)
        codigo += self.getLabel(lSalida)
        codigo += self.assigHeapH("-1")
        codigo += self.masHeap()

        '''
        L1
        guardarCadenas
        if(a==-1) goto L2
        goto L1
        L2
        guardarCadena2
        if(a==-1)goto L3
        goto L2
        L3:
        '''
        return {'heap': temp["temporal"], 'codigo': codigo}

    def concatenaString(self, c1, c2):
        temp = self.newTemp()
        codigo = ""
        tempo = self.newTemp()
        Ltemp = self.newTemp()
        loop = self.newLabel()
        lSalida = self.newLabel()
        tempo2 = self.newTemp()
        Ltemp2 = self.newTemp()
        loop2 = self.newLabel()
        lSalida2 = self.newLabel()
        codigo += self.assigTemp1(temp["temporal"], 'H')
        codigo += self.assigTemp1(tempo["temporal"], c1)
        codigo += self.getLabel(loop)
        codigo += self.getHeap(Ltemp["temporal"], tempo["temporal"])
        codigo += self.getCond2(Ltemp["temporal"], "==", "-1.0", lSalida)
        codigo += self.assigHeapH(Ltemp["temporal"])
        codigo += self.masHeap()
        codigo += self.assigTemp2(tempo["temporal"],
                                  tempo["temporal"], "+", "1")
        codigo += self.goto(loop)
        codigo += self.getLabel(lSalida)
        codigo += self.assigTemp1(tempo2["temporal"], c2)
        codigo += self.getLabel(loop2)
        codigo += self.getHeap(Ltemp2["temporal"], tempo2["temporal"])
        codigo += self.getCond2(Ltemp2["temporal"], "==", "-1.0", lSalida2)
        codigo += self.assigHeapH(Ltemp2["temporal"])
        codigo += self.masHeap()
        codigo += self.assigTemp2(tempo2["temporal"],
                                  tempo2["temporal"], "+", "1")
        codigo += self.goto(loop2)
        codigo += self.getLabel(lSalida2)
        codigo += self.assigHeapH("-1")
        codigo += self.masHeap()
        '''
        L1
        guardarCadenas
        if(a==-1) goto L2
        goto L1
        L2
        guardarCadena2
        if(a==-1)goto L3
        goto L2
        L3:
        '''
        return {'heap': temp["temporal"], 'codigo': codigo}
