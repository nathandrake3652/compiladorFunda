import copy
from enum import Enum

class TIPO_DATO(Enum) :
    NUMERO = 'numero'
    FUNCION = 'funcion'
    LISTA = 'lista'
    TEXTO = 'texto'
    BOOLEANO = 'booleano'

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo, valor) :
        self.id = id
        self.tipo = tipo
        self.valor = valor

class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = {}, deepcopy = False) :
        if deepcopy:
            self.simbolos = copy.deepcopy(simbolos)
        else:
            self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo
    
    def obtener(self, id : str) -> Simbolo:
        if not id in self.simbolos :
            print('Error: variable ', id, ' no definida.')

        return self.simbolos[id]

    def actualizar(self, simbolo) :
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo