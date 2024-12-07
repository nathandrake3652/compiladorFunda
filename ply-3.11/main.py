import os
import sys
from Instrucciones.Instruccion import *
import gramatica as g
import ts as TS




def main():

    if len(sys.argv) != 2:
        print("Sintaxis: py main.py [archivo]")
        sys.exit(1)
    
    archivo =  "pruebas/" + sys.argv[1]

    if not os.path.exists(archivo) :
        print(f"Error: el archivo '{archivo}' no existe")
        sys.exit(1)
    

    f = open(archivo, "r", encoding="utf-8")

    input = f.read()
    instrucciones = g.parse(input)


    ts_global = TS.TablaDeSimbolos()
    Instruccion.procesar_instrucciones(instrucciones, ts_global)


if __name__ == "__main__":
    main()


'''
def procesar_definicion_funcion(instr, ts):
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.FUNCION.value, instr)
    ts.agregar(simbolo)

def procesar_llamada_funcion(instr : Instruccion, ts):
    simbolo = ts.obtener(instr.id)

    if not(simbolo):
        print('Funcion no definida')
        return 

    if isinstance(simbolo.valor, Funcion):
        funcion = simbolo.valor
        if len(funcion.lista_parametros) != len(instr.parametros):
            print('Error: El número de argumentos no coincide')
            return
    ts_local = TS.TablaDeSimbolos(ts.simbolos)

    for i in range(len(funcion.lista_parametros)):
        parametro_valor = resolver_expresion_aritmetica(instr.parametros[i], ts)
        simbolo_parametro = TS.Simbolo(funcion.lista_parametros[i], TS.TIPO_DATO.NUMERO, parametro_valor)
        ts_local.agregar(simbolo_parametro)

    return procesar_instrucciones(funcion.instrucciones, ts_local)

def procesar_return(instr, ts):
    valor_retornado = resolver_expresion_aritmetica(instr.expresion, ts)
    return valor_retornado

def procesar_acceso_lista(expNum: ExpresionAccesoLista, ts):
    lista = ts.obtener(expNum.id).valor
    indice = resolver_expresion_aritmetica(expNum.indice, ts)
    if isinstance(lista, list) and 0 <= indice < len(lista):
        return lista[indice]
    else:
        print(f'Error: índice {indice} fuera de rango para la listsa {expNum.id}')

def procesar_definicion_lista(instr, ts):
    lista = []
    for contenido in instr.contenidos:
        val = resolver_expresion_aritmetica(contenido, ts)
        lista.append(val)
    return lista

def procesar_append_lista(instr : AppendLista, ts):
    lista_asignacion = ts.obtener(instr.lista_asig_id)

    if not(lista_asignacion):
        print('Lista asignación es nula')
        return 
    
    lista_parametro = ts.obtener(instr.lista_par_id)

    if lista_asignacion and isinstance(lista_parametro.valor, list):
        elemento = resolver_expresion_aritmetica(instr.elemento, ts)
        lista_parametro.valor.append(elemento)
        lista_asignacion.valor = lista_parametro.valor.copy()
        ts.actualizar(lista_asignacion)
    else:
        print(f'Error: "{instr.lista_par_id}" no es una lista válida')


def procesar_eliminar_lista(instr : EliminarLista, ts):
    lista_simbolo = ts.obtener(instr.id)
    if lista_simbolo and isinstance(lista_simbolo.valor, list):
        indice = resolver_expresion_aritmetica(instr.indice, ts)
        if 0 <= indice < len(lista_simbolo.valor):
            del lista_simbolo.valor[indice]
            ts.actualizar(lista_simbolo)
        else:
            print(f'Error: Índice {indice} fuera de rango en la lista "{instr.lista_id}".')
    else:
        print(f'Error: "{instr.lista_id}" no es una lista válida.')

#Cristian

def procesar_imprimir(instr, ts) :
    print('> ', resolver_cadena(instr.cad, ts))

    
def procesar_definicion(instr : Definicion, ts) :
    context = ContextoDefinicion()
    context.procesar_definicion(instr, ts)

def procesar_asignacion(instr : Asignacion, ts) :
    context = ContextoAsignacion()
    context.procesar_asignacion(instr, ts)

def procesar_mientras(instr, ts) :
    while resolver_expresion_logica(instr.expLogica, ts) :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_if(instr, ts) :
    val = resolver_expresion_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_if_else(instr, ts) :
    val = resolver_expresion_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfVerdadero, ts_local)
    else :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfFalso, ts_local)

def resolver_cadena(expCad : ExpresionCadena, ts) :
    return expCad.resolver_expresion(ts)

def resolver_expresion_logica(expLog : ExpresionLogica, ts) :
    return expLog.resolver_expresion(ts)

def resolver_expresion_aritmetica(expNum : ExpresionNumerica, ts : TablaDeSimbolos) :
    return expNum.resolver_expresion(ts)







def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    for instr in instrucciones :
        if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
        elif isinstance(instr, Definicion) : procesar_definicion(instr, ts)
        elif isinstance(instr, Asignacion) : procesar_asignacion(instr, ts)
        elif isinstance(instr, While) : procesar_mientras(instr, ts)
        elif isinstance(instr, If) : procesar_if(instr, ts)
        elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
        elif isinstance(instr, Funcion) : procesar_definicion_funcion(instr, ts) # Cristian
        elif isinstance(instr, LlamadaFuncion): procesar_llamada_funcion(instr, ts) # Cristian
        elif isinstance(instr, Return): return procesar_return(instr, ts) # Cristian
        elif isinstance(instr, AppendLista): procesar_append_lista(instr, ts) # Cristian
        elif isinstance(instr, EliminarLista): procesar_eliminar_lista(instr, ts) # Cristian
        else : print('Error: instrucción no válida')

'''



# resolver_expresion_logica
'''
    if(isinstance(expLog, ExpresionLogicaUnaria)):
        return expLog.exp
    
    exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
    exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)
    if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : return exp1 > exp2
    if expLog.operador == OPERACION_LOGICA.MENOR_QUE : return exp1 < exp2
    if expLog.operador == OPERACION_LOGICA.IGUAL : return exp1 == exp2
    if expLog.operador == OPERACION_LOGICA.DIFERENTE : return exp1 != exp2
'''

# resolver_expresion_numerica
'''
    resolver_expresion(expNum, ts)
    if isinstance(expNum, ExpresionBinaria) :
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        if expNum.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
        if expNum.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
        if expNum.operador == OPERACION_ARITMETICA.POR : return exp1 * exp2
        if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : return exp1 / exp2
    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return exp * -1
    elif isinstance(expNum, ExpresionNumero) :
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id).valor
    elif isinstance(expNum, ExpresionLista): # Cristian
        return procesar_definicion_lista(expNum, ts) # Cristian
    elif isinstance(expNum, LlamadaFuncion) :  # Cristian
        return procesar_llamada_funcion(expNum, ts) # Cristian
    elif isinstance(expNum, ExpresionAccesoLista): # Cristian
        return procesar_acceso_lista(expNum, ts)
'''

# resolver expresion_cadena
'''
        if isinstance(expCad, ExpresionConcatenar) :
        exp1 = resolver_cadena(expCad.exp1, ts)
        exp2 = resolver_cadena(expCad.exp2, ts)
        return exp1 + exp2
        elif isinstance(expCad, ExpresionDobleComilla) :
            return expCad.val
        elif isinstance(expCad, ExpresionCadenaNumerico) :
            return str(resolver_expresion_aritmetica(expCad.exp, ts))
        else :
            print('Error: Expresión cadena no válida')
'''


