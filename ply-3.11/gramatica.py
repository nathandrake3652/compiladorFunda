import logging

logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()



reservadas = {
    'lista' : 'LISTA',
    'numero' : 'NUMERO',
    'booleano' : 'BOOLEANO',
    'texto' : 'TEXTO',
    'imprimir' : 'IMPRIMIR',
    'mientras' : 'MIENTRAS',
    'if' : 'IF',
    'else' : 'ELSE',
    'def' : 'DEF', 
    'return' : 'RETURN', 
    'append' : 'APPEND',
    'del' : 'DEL',
    'True' : 'TRUE',
    'False' : 'FALSE',
    'for' : 'FOR'
}

tokens  = [
    'COMA',
    'CORIZQ',
    'CORDER',
    'PTCOMA',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'CONCAT',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'OR',
    'AND',
    'NOT',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_OR = r'\|\|'
t_AND = r'&&'
t_IGUAL = r'='
t_CONCAT = r'&'
t_NOT = r'!'
t_COMA = r',' 
t_CORDER = r'\]' 
t_CORIZQ = r'\[' 

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_TRUE(t):
    r'True'
    t.value = True
    return t

def t_FALSE(t):
    r'False'
    t.value = False
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'//[^\n]*'
    pass

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico

import sys
import ply.lex as lex
lexer = lex.lex(debug=True,debuglog=log)


# Asociación de operadores y precedencia
precedence = (
    ('left', 'COMA'),
    ('left', 'CONCAT'),
    ('left', 'AND', 'OR'),
    ('left', 'MAYQUE', 'MENQUE', 'IGUALQUE', 'NIGUALQUE'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('right', 'UMENOS', 'NOT'),
)



from Expresiones.expresiones import *
from Instrucciones.Instruccion import *


def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      : imprimir_instr
                        | definicion_instr
                        | asignacion_instr
                        | mientras_instr
                        | if_instr
                        | if_else_instr
                        | def_funcion_instr
                        | return_instr
                        | llamada_funcion_instr
                        | append_instr
                        | del_instr
                        | for_instr''' # Cristian
    t[0] = t[1]



def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ expresion PARDER PTCOMA'
    t[0] =Imprimir(t[3])

def p_tipo_def(t):
    '''tipo_def         : NUMERO 
                        | LISTA 
                        | BOOLEANO
                        | TEXTO'''
    t[0] = t[1]

def p_tipo_def_id(t):
    '''tipo_def : ID'''
    raise TypeError(f'No existe el tipo: {t[1]}') # Puede causar errores

def p_instruccion_definicion(t) :
    '''definicion_instr   : tipo_def ID PTCOMA
                          | tipo_def ID IGUAL valor_asignacion PTCOMA'''
    if len(t) == 4: #Sin asignacion
        t[0] = Definicion(t[2], t[1])
    else:
        t[0] =Definicion(t[2], t[1], t[4])

def p_asignacion_instr(t) :
    '''asignacion_instr : ID IGUAL valor_asignacion PTCOMA
                        | expresion_acceso_lista IGUAL valor_asignacion PTCOMA'''
    if  not isinstance(t[1], ExpresionAccesoLista):  
        t[0] = Asignacion(t[1], t[3])
    else:  
        t[0] = AsignacionLista(t[1], t[3])

def p_valor_asignacion(t) :
    '''valor_asignacion : expresion'''
    t[0] = t[1]


def p_expresion(t):
    '''expresion : expresion_numerica
                 | expresion_logica
                 | expresion_concatenar
                 | expresion_acceso_lista
                 | llamada_funcion_expr
                 | expresion_agrupada
                 | constantes
                 | expresion_lista
                 | id'''
    t[0] = t[1]

def p_expresion_agrupada(t):
    '''expresion_agrupada : PARIZQ expresion PARDER'''
    t[0] = t[2]

def p_constantes(t):
    '''constantes : ENTERO
                  | DECIMAL
                  | CADENA'''
    if isinstance(t[1], int) or isinstance(t[1], float):
        t[0] = ExpresionNumero(t[1])
    elif isinstance(t[1], str):
        t[0] = ExpresionDobleComilla(t[1])


def p_id(t):
    '''id : ID'''
    t[0] = ExpresionIdentificador(t[1])


def p_mientras_instr(t) :
    'mientras_instr     : MIENTRAS PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] =While(t[3], t[6])

def p_for_instr(t):
    'for_instr : FOR PARIZQ definicion_instr expresion_logica PTCOMA asignacion_instr PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] = For(t[3], t[4], t[6], t[9])


def p_if_instr(t) :
    'if_instr           : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER'
    t[0] =If(t[3], t[6])

def p_if_else_instr(t) :
    'if_else_instr      : IF PARIZQ expresion_logica PARDER LLAVIZQ instrucciones LLAVDER ELSE LLAVIZQ instrucciones LLAVDER'
    t[0] =IfElse(t[3], t[6], t[10])

def p_expresion_binaria(t):
    '''expresion_numerica : expresion MAS expresion
                        | expresion MENOS expresion
                        | expresion POR expresion
                        | expresion DIVIDIDO expresion'''
    if t[2] == '+'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    elif t[2] == '*': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR)
    elif t[2] == '/': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)

def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion %prec UMENOS'
    t[0] = ExpresionNegativo(t[2])



def p_expresion_concatenar(t):
    '''expresion_concatenar : expresion CONCAT expresion'''
    t[0] = ExpresionConcatenar(t[1], t[3])


def p_expresion_logica_binaria(t) :
    '''expresion_logica : expresion MAYQUE expresion
                        | expresion MENQUE expresion
                        | expresion IGUALQUE expresion
                        | expresion NIGUALQUE expresion
                        | expresion OR expresion
                        | expresion AND expresion'''
    if t[2] == '>'    : t[0] = ExpresionLogicaBinaria(t[1], t[3], OPERACION_LOGICA.MAYOR_QUE)
    elif t[2] == '<'  : t[0] = ExpresionLogicaBinaria(t[1], t[3], OPERACION_LOGICA.MENOR_QUE)
    elif t[2] == '==' : t[0] = ExpresionLogicaBinaria(t[1], t[3], OPERACION_LOGICA.IGUAL)
    elif t[2] == '!=' : t[0] = ExpresionLogicaBinaria(t[1], t[3], OPERACION_LOGICA.DIFERENTE)
    elif t[2] == '||' : t[0] = ExpresionLogicaBinaria(t[1], t[3], OPERACION_LOGICA.OR)
    elif t[2] == '&&' : t[0] = ExpresionLogicaBinaria(t[1], t[3], OPERACION_LOGICA.AND)
    else:
        raise SyntaxError(f'Error de sintaxis: {t}')

def p_expresion_logica_unaria(t) :
    '''expresion_logica : TRUE
                        | FALSE
                        | NOT expresion'''
    if(len(t) == 2):
        t[0] = ExpresionLogicaUnaria(t[1], None)
    else:
        t[0] = ExpresionLogicaUnaria(t[2], OPERACION_LOGICA.NOT)

#Cristian
def p_empty(t):
    'empty :'
    pass

def p_def_funcion_instr(t):
    '''def_funcion_instr : DEF ID PARIZQ lista_parametros PARDER LLAVIZQ instrucciones LLAVDER'''
    t[0] = Funcion(t[2], t[4], t[7])

def p_lista_parametros(t):
    '''lista_parametros : parametros
                        | empty'''
    if t[1] is not None:
        t[0] = t[1]
    else:
        t[0] = []

def p_parametros(t):
    '''parametros : parametros COMA tipo_def ID
                  | tipo_def ID'''
    if len(t) == 3:
        t[0] = [(t[2], t[1])]
    else:
        t[0] = t[1] + [(t[4], t[3])]



def p_return_instr(t):
    '''return_instr     : RETURN expresion PTCOMA
                        | RETURN PTCOMA'''
    if(len(t) == 3):
        t[0] = Return()
    else:
        t[0] = Return(t[2])

def p_lista_expresiones(t):
    '''lista_expresiones : lista_expresiones COMA expresion
                         | expresion'''
    if len(t) == 2:
        t[0] = [t[1]] 
    else:
        t[1].append(t[3])
        t[0] = t[1]


def p_llamada_funcion_expr(t):
    '''llamada_funcion_expr : ID PARIZQ lista_expresiones PARDER 
                       | ID PARIZQ PARDER'''
    if len(t) == 4:
        t[0] = LlamadaFuncion(t[1], [])
    else:
        t[0] = LlamadaFuncion(t[1], t[3])

def p_llamada_funcion_instr(t):
    '''llamada_funcion_instr : ID PARIZQ lista_expresiones PARDER PTCOMA
                             | ID PARIZQ PARDER PTCOMA'''
    if len(t) == 5:
        t[0] = LlamadaFuncion(t[1], [])
    else:
        t[0] = LlamadaFuncion(t[1], t[3])


def p_expresion_lista(t):
    '''expresion_lista : CORIZQ lista_expresiones CORDER
                       | CORIZQ CORDER'''
    if len(t) == 3:  
        t[0] = ExpresionLista([])
    else:            
        t[0] = ExpresionLista(t[2])


def p_expresion_acceso_lista(p):
    '''expresion_acceso_lista : ID CORIZQ expresion CORDER'''

    p[0] = ExpresionAccesoLista(p[1], p[3])




def p_append_lista(p):
    '''append_instr : ID IGUAL APPEND PARIZQ ID COMA expresion PARDER PTCOMA'''

    p[0] = AppendLista(p[1], p[5], p[7])

def p_del_lista(p):
    '''del_instr : DEL ID CORIZQ expresion CORDER PTCOMA'''

    p[0] = EliminarLista(p[2], p[4])

#Cristian

def p_error(t):
    if t is None:
        return
    print(t)
    raise SyntaxError("Error sintáctico en '%s'" % t.value)

def t_eof(t):
    return None

import ply.yacc as yacc
parser = yacc.yacc(debug=True,debuglog=log)


def parse(input) :
    return parser.parse(input)