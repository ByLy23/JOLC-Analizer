class NodoAST():
    def __init__(self, valor):
        self.listaNodos = []
        self.valor = valor

    def agregar(self, hijo, ambito=None, operador=None):
        if (hijo != None):
            if ambito != None:
                if ambito == 'ar':
                    if operador == 0:
                        hijo = '+'
                    if operador == 1:
                        hijo = '-'
                    if operador == 2:
                        hijo = '*'
                    if operador == 3:
                        hijo = '/'
                    if operador == 4:
                        hijo = '^'
                    if operador == 5:
                        hijo = '%'
                elif ambito == 'log':
                    if operador == 0:
                        hijo = '||'
                    if operador == 1:
                        hijo = '&&'
                    if operador == 2:
                        hijo = '!'
                elif ambito == 'rel':
                    if operador == 0:
                        hijo = '=='
                    if operador == 1:
                        hijo = '!='
                    if operador == 2:
                        hijo = '>'
                    if operador == 3:
                        hijo = '<'
                    if operador == 4:
                        hijo = '>='
                    if operador == 5:
                        hijo = '<='
            self.listaNodos.append(NodoAST(hijo))

    def getValor(self):
        return self.valor

    def getHijos(self):
        return self.listaNodos
