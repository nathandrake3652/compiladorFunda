# CompiladorFunda

Proyecto Compilador - Piton1.1

Integrantes: Donovan Almendares, Francisco Astudillo, Cristian Nettle
#Descripcion De gramatica
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


## Analisis Sintacticos
  se definieron el orden de operaciones booleanas y papomudas correspondientes 

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

## Ejecucion del compilador
  -Python Main.py //para ejecutar el programa abriendo el archivo desde el main
  py main.py [archivo] // para probar cada archivo 1 por 1
    
