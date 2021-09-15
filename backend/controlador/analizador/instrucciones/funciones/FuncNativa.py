from controlador.analizador.simbolos.Simbolo import Simbolo
from controlador.analizador.excepciones.Error import Error
from controlador.analizador.simbolos.Tipo import TipoDato
from controlador.analizador.abstracto.Instruccion import Instruccion
from math import *


class FuncNativa(Instruccion):
    def __init__(self, nombre, argumentos, linea, columna):
        super().__init__(TipoDato.ENTERO, linea, columna)
        self.nombre = nombre
        self.argumentos = argumentos

    def interpretar(self, arbol, tablaSimbolo):
        exp = self.nombre
        if isinstance(exp, Error):
            return exp
        if self.argumentos["exp2"] != None:
            if not self.argumentos["string"]:
                arg1 = self.argumentos["exp1"].interpretar(arbol, tablaSimbolo)
                if isinstance(arg1, Error):
                    return arg1
            else:
                arg1 = self.argumentos["exp1"]
            arg2 = self.argumentos["exp2"].interpretar(arbol, tablaSimbolo)
            if isinstance(arg2, Error):
                return arg2
            # ARGUMENTO
            if exp == "parse":
                if self.argumentos["exp2"].tipo == TipoDato.CADENA:
                    if arg1 == "Int64":
                        self.tipo = TipoDato.ENTERO
                        return int(arg2)
                    elif arg1 == "Float64":
                        self.tipo = TipoDato.DECIMAL
                        return float(arg2)
                    else:
                        return Error("Error Semantico", "No se puede parsear a un tipo de dato diferente", self.linea, self.columna)
                else:
                    return Error("Error Semantico", "El tipo de dato a parsear no es cadena", self.linea, self.columna)

            elif exp == "log":
                if self.comprobarExpresiones(self.argumentos["exp1"].tipo, self.argumentos["exp2"].tipo):
                    return log(arg2, arg1)
                else:
                    return Error("Error Semantico", "El tipo de dato debe ser entero o decimal", self.linea, self.columna)
            elif exp == "push":
                if self.argumentos["exp1"].tipo == TipoDato.ARREGLO:
                    self.tipo = TipoDato.ARREGLO
                    variable = tablaSimbolo.getVariable(
                        self.argumentos["exp1"].identificador)
                    if variable == None:
                        return Error("Error Semantico", "la variable {} no existe".format(self.identificador), self.linea, self.columna)
                    if variable.tipo != TipoDato.ARREGLO:
                        return Error("Error Semantico", "La variable debe ser de tipo arreglo", self.linea, self.columna)
                    for acceso in self.argumentos["exp1"].listaAccesos:
                        val = acceso.interpretar(arbol, tablaSimbolo)
                        if isinstance(val, Error):
                            return val
                        if acceso.tipo != TipoDato.ENTERO:
                            return Error("Error Semantico", "El tipo de dato debe ser entero", self.linea, self.columna)
                        try:
                            variable = variable.getValor()[str(val)]
                        except:
                            return Error("Error Semantico", "No se encontro el acceso", self.linea, self.columna)
                    exp = self.argumentos["exp2"].interpretar(
                        arbol, tablaSimbolo)
                    if isinstance(exp, Error):
                        return exp
                    print(variable.getValor())
                    try:
                        key = int(list(variable.getValor())[-1])+1
                        simbolo = Simbolo(
                            str(key), self.argumentos["exp2"].tipo, exp)
                        simbolo.tipoStruct = self.argumentos["exp2"].tipoStruct
                        simbolo.mutable = self.argumentos["exp2"].mutable
                        variable.getValor()[str(key)] = simbolo
                        # variable.tipo = self.expresion.tipo
                        # variable.tipoStruct = self.expresion.tipoStruct
                        # variable.mutable = self.expresion.mutable
                        # variable.setValor(exp)
                    except:
                        return Error("Error Semantico", "El acceso a variable no es arreglo", self.linea, self.columna)
                    #
                    # for expresion in self.argumentos["exp2"].expresiones:
                    #     val = expresion.interpretar(arbol, tablaSimbolo)
                    #     if isinstance(val, Error):
                    #         return val
                    #     simbolo = Simbolo(
                    #         str(key), expresion.tipo, val)
                    #     simbolo.tipoStruct = expresion.tipoStruct
                    #     simbolo.mutable = expresion.mutable
                    #     arg1[str(key)] = simbolo
                    #     key = key+1

            else:
                return Error("Error Semantico", "Comando no valido", self.linea, self.columna)
        else:
            arg1 = self.argumentos["exp1"].interpretar(arbol, tablaSimbolo)
            if isinstance(arg1, Error):
                return arg1
            if exp == "typeof":  # ARGUMENTO
                self.tipo = TipoDato.CADENA
                return str(self.argumentos["exp1"].tipo)[9:].capitalize()
            elif exp == "float":  # ARGUMENTO
                if self.argumentos["exp1"].tipo == TipoDato.ENTERO:
                    self.tipo = TipoDato.DECIMAL
                    return float(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser entero", self.linea, self.columna)
            elif exp == "string":  # ARGUMENTO
                if self.argumentos["exp1"].tipo == TipoDato.ARREGLO:
                    self.tipo = TipoDato.ARREGLO
                    return arg1
                self.tipo = TipoDato.CADENA
                return str(arg1)
            elif exp == "sqrt":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return sqrt(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
            elif exp == "log10":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return log10(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
            elif exp == "sin":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return sin(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
            elif exp == "cos":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return cos(arg1)
                else:
                    return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)
            elif exp == "tan":  # ARGUMENTO
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO or self.argumentos["exp1"].tipo != TipoDato.DECIMAL:
                    self.tipo = TipoDato.DECIMAL
                    return tan(arg1)
            elif exp == "length":
                if self.argumentos["exp1"].tipo != TipoDato.ENTERO:
                    return len(arg1)
                # else:
                #     return Error("Error Semantico", "No se puede sacar la longitud sino es arreglo", self.linea, self.columna)
            elif exp == "lowercase":
                if self.argumentos["exp1"].tipo == TipoDato.CADENA:
                    self.tipo = TipoDato.CADENA
                    return str(arg1).lower()
                else:
                    return Error("Error Semantico", "Debe ser un tipo de dato cadena", self.linea, self.columna)
            elif exp == "uppercase":
                if self.argumentos["exp1"].tipo == TipoDato.CADENA:
                    self.tipo = TipoDato.CADENA
                    return str(arg1).upper()
                else:
                    return Error("Error Semantico", "Debe ser un tipo de dato cadena", self.linea, self.columna)
            elif exp == "trunc":
                print("trunc")
                if self.argumentos["exp1"].tipo == TipoDato.DECIMAL:
                    self.tipo = TipoDato.ENTERO
                    return trunc(arg1)
                else:
                    return Error("Error Semantico", "El tipo de dato a parsear no es cadena", self.linea, self.columna)
            elif exp == "pop":
                if self.argumentos["exp1"].tipo == TipoDato.ARREGLO:
                    key = int(list(arg1)[-1])
                    val = arg1.pop(str(key))
                    if val.tipo == TipoDato.ARREGLO:
                        # print(val.valor)
                        vs = "pop: ["
                        for clave, valor in val.valor.items():
                            vs = vs+str(valor.valor)+","
                        vs = vs+"]"
                        return vs
                    return "pop: " + str(val.valor)
                else:
                    return Error("Error Semantico", "Un argumento no es valido", self.linea, self.columna)
            elif exp == "lenght":
                print("Escribi bien animal xd")
            else:
                return Error("Error Semantico", "Valor debe ser un dato numerico", self.linea, self.columna)

    def comprobarExpresiones(self, ar1, ar2):
        if ar1 == TipoDato.ENTERO or ar1 == TipoDato.DECIMAL:
            if ar2 == TipoDato.ENTERO or ar2 == TipoDato.DECIMAL:
                return True
        return False
