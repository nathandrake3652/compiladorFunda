from abc import ABC, abstractmethod
import ts as TS
from .Instruccion import Asignacion

class ProcesarAsignacionStrategy(ABC):
    @abstractmethod
    def procesar(self, instr : Asignacion, ts):
        pass

class ContextoAsignacion:
    def __init__(self):
        self.procesadores = {
            TS.TIPO_DATO.NUMERO.value : ProcesarAsignacionNumero(),
            TS.TIPO_DATO.LISTA.value : ProcesarAsignacionLista(),
            TS.TIPO_DATO.TEXTO.value : ProcesarAsignacionCadena(),
            TS.TIPO_DATO.BOOLEANO.value : ProcesarAsignacionBooleano(),
        }
    
    def procesar_asignacion(self, instr, ts):
        simbolo = ts.obtener(instr.id)
        if not simbolo:
            raise NameError(f"La variable '{instr.id}' no ha sido declarada")
        if simbolo.tipo not in self.procesadores:
            raise TypeError(f'Tipo de dato indefinido {simbolo.tipo} en: "{simbolo.id}"')
        procesador = self.procesadores[simbolo.tipo]
        procesador.procesar(instr, ts)

class ProcesarAsignacionNumero(ProcesarAsignacionStrategy):

    def procesar(self, instr : Asignacion, ts):
        val = instr.exp.resolver_expresion(ts)
        if not isinstance(val, int) and not isinstance(val, float):
            raise TypeError(f"Error de tipado: {instr.id} es de tipo numero")
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO.value, val)
        ts.actualizar(simbolo)
        
class ProcesarAsignacionLista(ProcesarAsignacionStrategy):
    def procesar(self, instr : Asignacion, ts):      
        val = instr.exp.resolver_expresion(ts)
        if not isinstance(val, list):
            raise TypeError(f"Error de tipado: {instr.id} es de tipo lista")
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.LISTA.value, val)
        ts.actualizar(simbolo)
class ProcesarAsignacionCadena(ProcesarAsignacionStrategy):

    def procesar(self, instr : Asignacion, ts):      
        val = instr.exp.resolver_expresion(ts)
        if not isinstance(val, str):
            raise TypeError(f"Error de tipado: {instr.id} es de tipo cadena")
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.TEXTO.value, val)
        ts.actualizar(simbolo)
class ProcesarAsignacionBooleano(ProcesarAsignacionStrategy):

    def procesar(self, instr : Asignacion, ts):      
        val = instr.exp.resolver_expresion(ts)
        if not isinstance(val, bool):
            raise TypeError(f"Error de tipado: {instr.id} es de tipo booleano")
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.BOOLEANO.value, val)
        ts.actualizar(simbolo)