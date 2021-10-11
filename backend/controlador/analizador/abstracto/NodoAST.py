class NodoAST():
    def __init__(self, valor):
        self.listaNodos = []
        self.valor = valor

    def agregar(self, hijo, ambito=None, op=None):
        if (hijo != None):
            if ambito != None:
                if ambito == 'ar':
                    operador = str(op)[13:]
                    if operador == 'MAS':
                        hijo = '+'
                    if operador == 'MENOS':
                        hijo = '-'
                    if operador == 'POR':
                        hijo = '*'
                    if operador == 'UMENOS':
                        hijo = '-'
                    if operador == 'DIVI':
                        hijo = '/'
                    if operador == 'POTENCIA':
                        hijo = '^'
                    if operador == 'MODULO':
                        hijo = '%'
                elif ambito == 'log':
                    operador = str(op)[9:]
                    if operador == 'OR':
                        hijo = '||'
                    if operador == 'AND':
                        hijo = '&&'
                    if operador == 'NOT':
                        hijo = '!'
                elif ambito == 'rel':
                    operador = str(op)[13:]
                    if operador == 'IGUAL':
                        hijo = '=='
                    if operador == 'DIFERENTE':
                        hijo = '!='
                    if operador == 'MAYOR':
                        hijo = '>'
                    if operador == 'MENOR':
                        hijo = '<'
                    if operador == 'MAYORIGUAL':
                        hijo = '>='
                    if operador == 'MENORIGUAL':
                        hijo = '<='
            self.listaNodos.append(NodoAST(hijo))

    def agregarAST(self, hijo):
        if hijo != None:
            self.listaNodos.append(hijo)

    def getValor(self):
        return self.valor

    def getHijos(self):
        return self.listaNodos
