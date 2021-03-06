from optimizador.analizador.abstracto.Instruccion import Instruccion
from optimizador.analizador.abstracto.Reporte import Reporte
from optimizador.analizador.instrucciones.AsignacionSimple import AsignacionSimple
from optimizador.analizador.instrucciones.Goto import Goto
from optimizador.analizador.instrucciones.If import If
from optimizador.analizador.instrucciones.Impresion import Impresion
from optimizador.analizador.instrucciones.Label import Label


class Funcion(Instruccion):
    def __init__(self, ide, instrucciones, linea, columna):
        super().__init__(linea, columna)
        self.ide = ide
        self.instrucciones = instrucciones

    def getInstruccion(self, arbol):
        # print(self.instrucciones)
        prueba = []
        codigo = ""
        self.regla1(arbol)
        self.regla24(arbol)
        self.regla3(arbol)
        self.regla5(arbol)
        for ins in self.instrucciones:
            prueba = ins.getInstruccion(arbol)
            codigo += prueba
            # print(prueba)
        return 'func '+self.ide+'(){\n'+codigo+'\n}\n'

    def getNormal(self):
        return 'func '+self.ide+'(){\n'+self.instrucciones+'\n}'

    def regla1(self, arbol):
        instrucciones = self.instrucciones
        cont = 0
        for i in self.instrucciones:
            if isinstance(instrucciones[cont], AsignacionSimple):
                if isinstance(instrucciones[cont+1], AsignacionSimple):
                    a1 = instrucciones[cont]
                    a2 = instrucciones[cont+1]
                    if a1.t1 == a2.t2 and a1.t2 == a2.t1:
                        reglaDesc = '{} = {};'.format(
                            a1.t1, a1.t2)+'{} = {};'.format(a1.t2, a1.t1)
                        reporte = Reporte(
                            'Mirilla Eliminacion de instrucciones redundantes', 'Regla 1', reglaDesc, '{} = {};'.format(a1.t1, a1.t2), instrucciones[cont].linea)
                        arbol.getReporte().append(reporte)
                        self.instrucciones.pop(cont-1)
            cont += 1

    def regla24(self, arbol):
        instrucciones = self.instrucciones
        cont = 0
        l = ""
        nuevasInstrucciones = []
        for i in self.instrucciones:
            if isinstance(instrucciones[cont], Goto):
                lTemporal = instrucciones[cont]
                l = lTemporal.label.getInstruccion(
                    arbol)[0:-2]  # guardamos el valor del label
                # guardamos las instrucciones que van despues del label
                for j in range(cont+1, len(self.instrucciones)):
                    nuevasInstrucciones.append(instrucciones[j])
                    # print(nuevasInstrucciones[j-1])
                    if j+1 > len(self.instrucciones)-1:  # verifica si la siguiente es nula
                        break
                    # si la siguiente instruccion es un label hace lo siguiente
                    if isinstance(instrucciones[j], Label):
                        if not isinstance(instrucciones[j+1], Goto):
                            # print(len(nuevasInstrucciones))
                            # otiene el valor del label
                            label = instrucciones[j].getInstruccion(arbol)[
                                0:-2]
                            if l != label:  # Si los valores son diferentes alv
                                # print('No son iguales')
                                nuevasInstrucciones = []
                                break
                            # si los valores si existen va a eliminar todas las etiquetas
                            for k in range(cont, j):
                                self.instrucciones.pop(cont)

                            reglaDesc = 'goto {};'.format(
                                l)+'<Instrucciones>'+'{}:'.format(l)
                            reporte = Reporte(
                                'Mirilla Eliminacion de codigo inalcanzable', 'Regla 2', reglaDesc, '{}:'.format(l), instrucciones[cont].linea)
                            arbol.getReporte().append(reporte)
                            # print('Son iguales')  # aca realizo la accion
                            break
                        else:
                            self.instrucciones[cont].label = instrucciones[j+1].label
                            reglaDesc = 'goto {};'.format(
                                l)+'<Instrucciones>'+'{}: goto {};'.format(l, instrucciones[j+1].label.getInstruccion(arbol)[0:-2])
                            reglaOpt = 'goto {};'.format(
                                instrucciones[j+1].label.getInstruccion(arbol)[0:-2])+'<Instrucciones>'+'{}: goto {};'.format(l, instrucciones[j+1].label.getInstruccion(arbol)[0:-2])
                            reporte = Reporte(
                                'Mirilla Optimizacion de flujo de control', 'Regla 4', reglaDesc, reglaOpt, instrucciones[cont].linea)
                            arbol.getReporte().append(reporte)
            cont += 1

    def regla3(self, arbol):
        instrucciones = self.instrucciones
        cont = 0
        for i in self.instrucciones:
            if isinstance(instrucciones[cont], If):
                l1 = instrucciones[cont].label.getInstruccion(arbol)[0:-2]
                if isinstance(instrucciones[cont+1], Goto):
                    l2 = instrucciones[cont +
                                       1].label.getInstruccion(arbol)[0:-2]
                    if isinstance(instrucciones[cont+2], Label):
                        lC = instrucciones[cont+2].getInstruccion(arbol)[0:-2]
                        if l1 == lC:
                            for j in range(cont+3, len(instrucciones)):
                                if isinstance(instrucciones[j], Label):
                                    lC2 = instrucciones[j].getInstruccion(arbol)[
                                        0:-2]
                                    if l2 == lC2:
                                        self.instrucciones[cont].rel = "!="
                                        self.instrucciones[cont].label = instrucciones[j]
                                        self.instrucciones.pop(cont+1)
                                        self.instrucciones.pop(cont+1)
                                        reglaDesc = 'if('+instrucciones[cont].op1+'=='+instrucciones[cont].op2 + \
                                            '){goto '+l1+';} goto '+l2+'; ' + \
                                            l1+': <Instrucciones> '+l2+':'
                                        reporte = Reporte(
                                            'Mirilla Optimizacion de flujo de control', 'Regla 3', reglaDesc, 'if('+instrucciones[cont].op1+'!='+instrucciones[cont].op2+'){goto '+l2+';} <Instrucciones> '+l2+':', instrucciones[cont].linea)
                                        arbol.getReporte().append(reporte)
                                    break
            cont += 1

    def regla5(self, arbol):
        instrucciones = self.instrucciones
        cont = 0
        for i in self.instrucciones:
            if isinstance(instrucciones[cont], If):
                if instrucciones[cont].rel == ('>', '<', ">=", '<='):
                    l1 = instrucciones[cont].label.getInstruccion(arbol)[0:-2]
                    for j in range(cont, len(instrucciones)):
                        if isinstance(instrucciones[j], Label):
                            lC = instrucciones[j].getInstruccion(arbol)[0:-2]
                            if l1 == lC:
                                if isinstance(instrucciones[j+1], Goto):
                                    l2 = instrucciones[j+1].label
                                    self.instrucciones[cont].label = l2
                                    reglaDesc = 'if('+instrucciones[cont].op1+instrucciones[cont].rel+instrucciones[cont].op2 + \
                                                '){goto '+l1+';} goto '+l2+'; ' + \
                                                l1+': <Instrucciones> '+l2+':'
                                    reporte = Reporte(
                                        'Mirilla Optimizacion de flujo de control', 'Regla 5', reglaDesc, 'if('+instrucciones[cont].op1+instrucciones[cont].rel+instrucciones[cont].op2+'){goto '+l2+';} <Instrucciones> '+l2+':', instrucciones[cont].linea)
                                    arbol.getReporte().append(reporte)
            cont += 1

    def if_integer(string):
        if(string[0]) == ('-', '+'):
            return string[1:].isDigit()
        return string.isDigit()
