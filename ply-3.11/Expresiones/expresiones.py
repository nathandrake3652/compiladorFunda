from enum import Enum
from abc import ABC, abstractmethod
from typing import Any, List

from ts import *

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4

class OPERACION_LOGICA(Enum) :
    MAYOR_QUE = 1
    MENOR_QUE = 2
    IGUAL = 3
    DIFERENTE = 4


class Expresion(ABC):
    '''
        Esta clase representa una expresión númerica
    '''
    @abstractmethod
    def resolver_expresion(self, ts : TablaDeSimbolos) -> Any:
        pass

class ExpresionNumerica(Expresion):
    '''
        Esta clase representa una expresión numérica
    '''

    @abstractmethod
    def resolver_expresion(self, ts) -> int | float:
        pass 



class ExpresionBinaria(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Binaria.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1 : Expresion, exp2 : Expresion, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
    
    def resolver_expresion(self, ts):
        exp1 = self.exp1.resolver_expresion(ts)
        exp2 = self.exp2.resolver_expresion(ts)

        if not isinstance(exp1, (int, float)) or not isinstance(exp2, (int, float)):
            raise TypeError("Operadores deben ser numéricos")
        
        if self.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
        if self.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
        if self.operador == OPERACION_ARITMETICA.POR : return exp1 * exp2
        if self.operador == OPERACION_ARITMETICA.DIVIDIDO : return exp1 / exp2
        else:
            raise TypeError('Error en resolver_expresion')

class ExpresionNegativo(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Negativa.
        Esta clase recibe la expresion
    '''
    def __init__(self, exp : Expresion) :
        self.exp = exp
    
    def resolver_expresion(self, ts):
        exp = self.exp.resolver_expresion(ts)

        if not isinstance(exp, (int, float)):
            raise TypeError("Operadores deben ser numéricos")
        return exp * -1


class ExpresionNumero(ExpresionNumerica) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

    def __init__(self, val = 0) :
        self.val = val
    
    def resolver_expresion(self, ts):
        return self.val

class ExpresionIdentificador(Expresion) :
    '''
        Esta clase representa un identificador.
    '''

    def __init__(self, id = "") :
        self.id = id
    
    def resolver_expresion(self, ts : TablaDeSimbolos):
        return ts.obtener(self.id).valor

class ExpresionCadena(Expresion):
    '''
        Esta clase representa una Expresión de tipo cadena.
    '''

    @abstractmethod
    def resolver_expresion(self, ts : TablaDeSimbolos) -> str:
        pass 


class ExpresionConcatenar(ExpresionCadena) :
    '''
        Esta clase representa una Expresión de tipo cadena.
        Recibe como parámetros las 2 expresiones a concatenar
    '''

    def __init__(self, exp1 : Expresion, exp2: Expresion) :
        self.exp1 = exp1
        self.exp2 = exp2 
    
    def resolver_expresion(self, ts):

        exp1 = self.exp1.resolver_expresion(ts)
        exp2 = self.exp2.resolver_expresion(ts)
        if (not isinstance(exp1, (int, float, str, bool, list))) or (not isinstance(exp2, (int, float, str, bool, list))):
                raise TypeError('Error de tipado, no es texto válido')        

        return str(exp1) + str(exp2)
    

class ExpresionDobleComilla(ExpresionCadena) :
    '''
        Esta clase representa una cadena entre comillas doble.
        Recibe como parámetro el valor del token procesado por el analizador léxico
    '''

    def __init__(self, val : str) :
        self.val = val
    
    def resolver_expresion(self, ts):
        return self.val

class ExpresionCadenaExpresion(ExpresionCadena) :
    '''
        Esta clase representa una expresión numérica tratada como cadena.
        Recibe como parámetro la expresión numérica
    '''
    def __init__(self, exp : Expresion) : #Cambiar para que acepte funciones
        self.exp = exp
    
    def resolver_expresion(self, ts):
        return str(self.exp.resolver_expresion(ts)) 

class ExpresionLogica(Expresion) :
    '''
        Esta clase representa la expresión lógica.
    '''

    @abstractmethod
    def resolver_expresion(self, ts) -> bool:
        pass 


class ExpresionLogicaBinaria(ExpresionLogica) :
    '''
        Esta clase representa una expresión logica binaria
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1: ExpresionNumerica, exp2 : ExpresionNumerica, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
    
    def resolver_expresion(self, ts):
        exp1 = self.exp1.resolver_expresion(ts)
        exp2 = self.exp2.resolver_expresion(ts)

        if not isinstance(exp1, (int, float)) or not isinstance(exp2, (int, float)):
            raise TypeError("Operadores deben ser numéricos")

        if self.operador == OPERACION_LOGICA.MAYOR_QUE : return exp1 > exp2
        if self.operador == OPERACION_LOGICA.MENOR_QUE : return exp1 < exp2
        if self.operador == OPERACION_LOGICA.IGUAL : return exp1 == exp2
        if self.operador == OPERACION_LOGICA.DIFERENTE : return exp1 != exp2 
        else:
            raise TypeError('Error de tipado en resolver expresion logica binaria')

class ExpresionLogicaUnaria(ExpresionLogica):
    '''
        Esta clase rpresenta una expresión lógica unaria
    '''

    def __init__(self, exp): # Funciona porque por ahora es o True o False, ya definido
        self.exp = exp
    

    def resolver_expresion(self, ts):
        return self.exp 

class ExpresionLista(Expresion):
    '''
        Esta clase representa la instrucción de crear una lista
    '''
    def __init__(self,contenidos : List[Expresion]):
        self.contenidos = contenidos
    
    def resolver_expresion(self, ts):
        lista = []
        for contenido in self.contenidos:
            val = contenido.resolver_expresion(ts)
            lista.append(val)
        return lista

class ExpresionAccesoLista(Expresion): 
    '''Esta clase representa el acceso a una lista'''

    def __init__(self, id, indice : ExpresionNumerica):
        self.id = id
        self.indice = indice 
    
    def resolver_expresion(self, ts):
        lista = ts.obtener(self.id).valor
        indice = self.indice.resolver_expresion(ts)

        if not isinstance(indice, int):
            raise TypeError("indice debe ser numero entero ")

        if isinstance(lista, list) and 0 <= indice < len(lista):
            return lista[indice]
        else:
            raise IndexError('Fuera de limites de la lista, o no es una lista')
