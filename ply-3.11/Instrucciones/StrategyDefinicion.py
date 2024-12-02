from abc import ABC, abstractmethod
import ts as TS
from .Instruccion import Definicion



class ContextoDefinicion:
    def __init__(self):
        self.procesadores = {
            TS.TIPO_DATO.NUMERO.value : ProcesarDefinicionNumero(),
            TS.TIPO_DATO.LISTA.value : ProcesarDefinicionLista(),
            TS.TIPO_DATO.TEXTO.value : ProcesarDefinicionCadena(),
            TS.TIPO_DATO.BOOLEANO.value : ProcesarDefinicionBooleano(),
        }
    
    def procesar_definicion(self, instr : Definicion, ts):
        if instr.tipo not in self.procesadores:
            raise TypeError(f'Tipo de dato indefinido {instr.tipo} en: "{instr.id}"')
        procesador = self.procesadores[instr.tipo]
        procesador.procesar(instr, ts)
class ProcesarDefinicionStrategy(ABC):
    
    @abstractmethod
    def procesar(self, instr : Definicion, ts):
        pass


class ProcesarDefinicionNumero(ProcesarDefinicionStrategy):

    def procesar(self, instr : Definicion, ts : TS.TablaDeSimbolos):
        val = 0
        if instr.expr != None:
            val = instr.expr.resolver_expresion(ts)

        if not isinstance(val, (int, float)):
            raise TypeError(f'Debe ser una expresión númerica (numero)')
        
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO.value, val)
        ts.agregar(simbolo)
class ProcesarDefinicionLista(ProcesarDefinicionStrategy):

    def procesar(self, instr : Definicion, ts):  
        val = []    
        if instr.expr != None:
            val = instr.expr.resolver_expresion(ts)
        
        if not isinstance(val, list):
            raise TypeError(f'Debe ser una expresión lista ([...])')
        
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.LISTA.value, val)
        ts.agregar(simbolo)
class ProcesarDefinicionCadena(ProcesarDefinicionStrategy):

    def procesar(self, instr : Definicion, ts): 
        val = ""     
        if instr.expr != None:
            val = instr.expr.resolver_expresion(ts)

        if not isinstance(val, str):
            raise TypeError(f'Debe ser una expresión cadena (texto)')
        


        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.TEXTO.value, val)
        ts.agregar(simbolo)
class ProcesarDefinicionBooleano(ProcesarDefinicionStrategy):

    def procesar(self, instr : Definicion, ts):  
        val = False   
        if instr.expr != None:
            val = instr.expr.resolver_expresion(ts)
        
        if not isinstance(val, bool):
            raise TypeError(f'Debe ser una expresión lógica (booleana)')
        
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.BOOLEANO.value, val)
        ts.agregar(simbolo)