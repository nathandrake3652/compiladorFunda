from Expresiones.expresiones import *
from abc import ABC, abstractmethod
import ts as TS

class Instruccion(ABC):
    '''This is an abstract class'''

    @abstractmethod
    def procesar_instruccion(self, ts):
        pass

    @staticmethod
    def procesar_instrucciones(instrucciones, ts):
        for instr in instrucciones:
            if not isinstance(instr, Instruccion):
                raise TypeError('Debería de ser una instrucción')
            resultado = instr.procesar_instruccion(ts)
            if isinstance(instr, Return):
                return resultado
            elif resultado is not None:
                return resultado


class Imprimir(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  cad : ExpresionCadena) :
        self.cad = cad
    
    def procesar_instruccion(self, ts):
        print('> ', self.cad.resolver_expresion(ts))




class Definicion(Instruccion) :
    '''
        Esta clase representa la instrucción de definición de variables.
        Recibe como parámetro el nombre del identificador a definir
    '''

    def __init__(self, id, tipo, expr : Expresion = None) :
        self.id = id
        self.tipo = tipo
        self.expr = expr
    
    def procesar_instruccion(self, ts):
        from .StrategyDefinicion import ContextoDefinicion  
        contextDef = ContextoDefinicion()
        contextDef.procesar_definicion(self, ts)

        
class Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, exp) :
        self.id = id
        self.exp = exp
    
    def procesar_instruccion(self, ts):
        from .StrategyAsignacion import ContextoAsignacion  
        contextAsig = ContextoAsignacion()
        contextAsig.procesar_asignacion(self, ts)
        
        
class While(Instruccion) : #while
    '''
        Esta clase representa la instrucción mientras.
        La instrucción mientras recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica : Expresion, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones
    
    def procesar_instruccion(self, ts):
        val = self.expLogica.resolver_expresion(ts)
        if not isinstance(val, bool):
            raise TypeError('El argumento del while debe ser booleano')

        while val:
            ts_local = TablaDeSimbolos(ts.simbolos)
            resultado = Instruccion.procesar_instrucciones(self.instrucciones, ts_local)
            if resultado is not None:
                return resultado
            val = self.expLogica.resolver_expresion(ts)
            if not isinstance(val, bool):
                raise TypeError('El argumento del while debe ser booleano')


class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if.
        La instrucción if recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica : Expresion, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones
    
    def procesar_instruccion(self, ts):
        val =  self.expLogica.resolver_expresion(ts)

        if not isinstance(val, bool):
            raise TypeError('El argumento del while debe ser booleano')
        
        if val:
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            resultado = Instruccion.procesar_instrucciones(self.instrucciones, ts_local)
            if resultado is not None:
                return resultado
        
class IfElse(Instruccion) : 
    '''
        Esta clase representa la instrucción if-else.
        La instrucción if-else recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera y otro lista de instrucciones
        a ejecutar si la expresión lógica es falsa.
    '''

    def __init__(self, expLogica : Expresion, instrIfVerdadero = [], instrIfFalso = []) :
        self.expLogica = expLogica
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso
    
    def procesar_instruccion(self, ts):
        val = self.expLogica.resolver_expresion(ts)

        if not isinstance(val, bool):
            raise TypeError('El argumento del while debe ser booleano')
        
        if val:
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            resultado = Instruccion.procesar_instrucciones(self.instrIfVerdadero, ts_local)
            if resultado is not None:
                return resultado
        else:
            ts_local = TS.TablaDeSimbolos(ts.simbolos)
            resultado = Instruccion.procesar_instrucciones(self.instrIfFalso, ts_local)
            if resultado is not None:
                return resultado


class Funcion(Instruccion) :
    '''
        Esta clase representa la intrucción definir Función
        La instrucción funcion resibe como parámetro el nombre de la función, lista de parametros, lista de instrucciones y lo que retorna
    '''

    def __init__(self, id, lista_parametros = [], instrucciones = []):
        self.id = id
        self.lista_parametros = lista_parametros
        self.instrucciones = instrucciones
    
    def procesar_instruccion(self, ts):
        simbolo = TS.Simbolo(self.id, TS.TIPO_DATO.FUNCION.value, self)
        ts.agregar(simbolo)

class Return(Instruccion) :
    '''
        Esta clase representa la instrucción Retorno
    '''
    def __init__(self, expresion : Expresion = None):
        self.expresion = expresion
    

    def procesar_instruccion(self, ts):
        if self.expresion == None:
            return None
        val = self.expresion.resolver_expresion(ts)
        if val == None:
            print("val es nulo puede generar errores")
            raise Expresion('No puede devolver None una expresion')
        return val
    


class LlamadaFuncion(Instruccion, Expresion): 
    '''
        Esta clase representa la instrucción o expresion llamada a función.
        Recibe como parámetros el id de la funcion y sus parametros.
    '''
    def __init__(self, id, parametros : List[Expresion] = []):
        self.parametros = parametros
        self.id = id
    
    def resolver_expresion(self, ts):
        val = self.procesar_instruccion(ts)
        if val is None:
            raise RuntimeError('La función no devuelve ningún valor')
        return val
    
    def procesar_instruccion(self, ts):
        simbolo = ts.obtener(self.id)

        if not(simbolo):
            raise NameError('Funcion no definida')
        if not isinstance(simbolo.valor, Funcion):
            raise TypeError('no es una función la variable', self.id)
        
        funcion = simbolo.valor 
        if len(funcion.lista_parametros) != len(self.parametros):
            raise SyntaxError('Error: El número de argumentos no coincide')
        
        ts_local = TS.TablaDeSimbolos(ts.simbolos, deepcopy=True)

        for i in range(len(funcion.lista_parametros)):
            parametro_valor = (self.parametros[i]).resolver_expresion(ts)
            simbolo_parametro = TS.Simbolo(funcion.lista_parametros[i], TS.TIPO_DATO.TEXTO, parametro_valor)
            ts_local.agregar(simbolo_parametro)
        
        resultado = Instruccion.procesar_instrucciones(funcion.instrucciones, ts_local)
        return resultado



class AppendLista(Instruccion):
    '''
        Esta clase represneta la instrucción para agregar un elemento a una lista
        Recibe el identificador de la lista, identificador de la otra lista y el elemento a agregar
    '''

    def __init__(self, lista_asig_id, lista_par_id, elemento : Expresion):
        self.lista_asig_id = lista_asig_id
        self.lista_par_id = lista_par_id
        self.elemento = elemento

    def procesar_instruccion(self, ts):
        lista_asignacion = ts.obtener(self.lista_asig_id)

        if not(lista_asignacion):
            print('Lista asignación es nula')
            return 
        
        lista_parametro = ts.obtener(self.lista_par_id)

        if lista_asignacion and isinstance(lista_parametro.valor, list):
            elemento = self.elemento.resolver_expresion(ts)
            lista_parametro.valor.append(elemento)
            lista_asignacion.valor = lista_parametro.valor.copy()
            ts.actualizar(lista_asignacion)
        else:
            print(f'Error: "{self.lista_par_id}" no es una lista válida')



class EliminarLista(Instruccion):
    '''
        Esta clase representa la instrucción para eliminar un elemento de una lista
    '''

    def __init__(self, id, indice : Expresion):
        self.id = id
        self.indice = indice

    def procesar_instruccion(self, ts):
        lista_simbolo = ts.obtener(self.id)
        if lista_simbolo and isinstance(lista_simbolo.valor, list):
            
            indice = self.indice.resolver_expresion(ts)
            if not isinstance(indice, int):
                raise ArithmeticError('El indice debe ser de tipo numerico entero')

            if 0 <= indice < len(lista_simbolo.valor):
                del lista_simbolo.valor[indice]
                ts.actualizar(lista_simbolo)
            else:
                print(f'Error: Índice {indice} fuera de rango en la lista "{self.lista_id}".')
        else:
            print(f'Error: "{self.lista_id}" no es una lista válida.')
            
