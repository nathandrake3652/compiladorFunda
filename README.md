# CompiladorFunda

Proyecto Compilador - Piton1.1

## Integrantes: 
    - Donovan Almendares
    - Francisco Astudillo 
    - Cristian Nettle

# Descripcion De gramatica
para la gramatica del lenguaje no hubo cambios significativos salvo para las funciones whiles y asignacion de variables primitivas las cuales se mostraran a continuacion


Compilador Utilizando ply
# Analisis Lexico
# Funciones booleanas 


## condicionales:
    if  
    else 
    ciclos:
    while → mientras
    for
    if else

## Tipos de datos 
    int  → numero
    String  → nexto 
    bool  → booleano 
    array  → lista

# Tokens
### **Tokens Aritméticos**
| Token       | Símbolo    |
|-------------|------------|
| `MAS`       | `+`        |
| `MENOS`     | `-`        |
| `POR`       | `*`        |
| `DIVIDIDO`  | `/`        |
| `MENQUE`    | `<`        |
| `MAYQUE`    | `>`        |
| `IGUALQUE`  | `==`       |
| `MODULO`    | `%`        | 
| `NIGUALQUE` | `!=`       |
| `DECIMAL`   | *(número decimal)* |
| `ENTERO`    | *(número entero)*  |

---

### **Tokens Lógicos**
| Token       | Símbolo    |
|-------------|------------|
| `OR`        | `\|\|`       |
| `AND`       | `&&`       |
| `NOT`       | `!`        |

---

### **Tokens Otros**
| Token       | Símbolo    |
|-------------|------------|
| `COMA`      | `,`        |
| `CORIZQ`    | `[`        |
| `CORDER`    | `]`        |
| `PTCOMA`    | `;`        |
| `LLAVIZQ`   | `{`        |
| `LLAVDER`   | `}`        |
| `PARIZQ`    | `(`        |
| `PARDER`    | `)`        |
| `IGUAL`     | `=`        |
| `CONCAT`    | `&`        |
| `CADENA`    | *(cadena de texto)* |
| `ID`        | *(identificador)*   |

### **Palabras Reservadas**

| Palabra Clave | Token       |
|---------------|-------------|
| `lista`       | `LISTA`     |
| `numero`      | `NUMERO`    |
| `booleano`    | `BOOLEANO`  |
| `texto`       | `TEXTO`     |
| `imprimir`    | `IMPRIMIR`  |
| `mientras`    | `MIENTRAS`  |
| `if`          | `IF`        |
| `else`        | `ELSE`      |
| `def`         | `DEF`       |
| `return`      | `RETURN`    |
| `append`      | `APPEND`    |
| `del`         | `DEL`       |
| `True`        | `TRUE`      |
| `False`       | `FALSE`     |
| `for`         | `FOR`       |



## Analisis Sintacticos
  se definieron el orden de operaciones booleanas y papomudas correspondientes 

  ### **Orden de Precedencia**

| Nivel de Precedencia | Asociatividad | Operadores                         |
|-----------------------|---------------|-------------------------------------|
| 1 (más bajo)          | Izquierda     | `COMA`                             |
| 2                     | Izquierda     | `CONCAT`                           |
| 3                     | Izquierda     | `AND`, `OR`                        |
| 4                     | Izquierda     | `MAYQUE`, `MENQUE`, `IGUALQUE`, `NIGUALQUE` |
| 5                     | Izquierda     | `MAS`, `MENOS`                     |
| 6                     | Izquierda     | `POR`, `DIVIDIDO`, `MODULO`        |
| 7 (más alto)          | Derecha       | `UMENOS`, `NOT`                    |


### **Producción del Ciclo For**

El ciclo `for` permite iterar sobre un rango de valores definido por una inicialización, una condición, y una actualización. A continuación, se presenta la producción correspondiente:

```python
def p_for_instr(t):
    '''for_instr : FOR PARIZQ definicion_instr expresion_logica PTCOMA asignacion_instr PARDER LLAVIZQ instrucciones LLAVDER'''
    t[0] = For(t[3], t[4], t[6], t[9])
```
Ejemplo:
```
for (numero i = 0; i < 10; i = i + 1;) {
    imprimir("Valor de i: " & i);
}
```

## Asignaciones
  se definieron tipos primitivos(enteros, string,etc) y complejos(listas )
  las listas tienen soporte al estar vacias y pueden ser modificadas con indices 
  
## Operaciones Aritméticas

  Operadores básicos: suma, resta, multiplicación, división, módulo.
  Se maneja la division entre 0

  
## Operaciones Booleanas
  Se implementaron las operadores booleanas en su totalidad(and, or,<, >, ==,etc.)
  Valores booleanos implementados
    
## Funciones
  se definieron funciones con y sin valores de entrada y con sus return respectivos

## impresion
  se definio la funcion Imprimir la cual hace de print
  
## Dependencias
  pip install ply

## **Ejecución del Compilador**
Debes estar ubicado en el directorio `ply-3.11` y ejecutar el siguiente comando:
### Para ejecutar el programa desde el directorio `ply-3.11`:
```cmd
py main.py [archivo.txt]
```
### Archivos disponibles para pruebas:
```plaintext
ciclos.txt
condicionales.txt
errores.txt
funciones.txt
listas.txt
```

