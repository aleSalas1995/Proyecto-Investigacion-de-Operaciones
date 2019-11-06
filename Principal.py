import argparse
import sys
import re # Expresiones regualres

#Variables globales
global tipoDeOptimizacion;
global numeroVariablesDecision;
global numeroRestricciones;
global variableU

#  Import de clases
from Controlador import*
from Imprimir import*

coeficientesFuncionObjetivo = []
restricciones = []

#Funcion Main
def main(elementosEntrada):#elementosEntrada):

    global coeficientesFuncionObjetivo
    global restricciones

    archivoSalida = "solucionDosFases"
    #Leer el archivo de archivoEntrada
    #elementosEntrada = ['min', '3,2', '2,3,1','1,4,2,8,>=', '3,2,0,6,>=']
    #['max','2,3','3,5','1,0,4,<=','0,2,12,<=','3,2,18,='] 36
    #['max','2,2','3,5','1,0,4,<=','0,2,12,<='] 42
    #['min', '3,2', '160,120,280', '2,1,4,1,>=', '2,2,2,1.5,>='] 100
    #['min','2,2','2000,500','2,3,36,>=','3,6,60,>='] 6000
    #['max', '3,2', '2,3,5', '1,4,2,8,>=', '3,2,0,6,>='] 19
    #['max','2,3','3,5','1,0,4,<=','0,2,12,<=','3,2,18,='] 36
    #['min','2,2','-2,-3','1,1,15,<=','1,2,20,<='] -35
    #['max','3,4','20,10,15','3,2,5,55,<=','2,1,1,26,<=','1,1,1,30,<=','5,2,4,57,<='] 268
    #['min', '3,2', '2,3,1','1,4,2,8,>=', '3,2,0,6,>='] 7
    #['max','4,2','4,2,3,5','2,3,4,2,300,=','8,1,1,5,300,='] 400
    #['max','4,3','3,-1,3,4','1,2,2,4,40,<=','2,-1,1,2,8,<=','4,-2,1,-1,10,<='] 36
    #leerArchivoEntrada(archivoEntrada) #Aqui entra la lista de Ale
    asignarElementos(elementosEntrada)

    global numeroVariablesDecision
    file = Archivo(archivoSalida)

    controlador = Controlador(tipoDeOptimizacion,coeficientesFuncionObjetivo,restricciones,int(numeroVariablesDecision),file.getArchivo(),False)
    controlador.inicioControlador()
    float

def fname(arg):
    pass

def mainDual(elementosEntrada, file):

    global coeficientesFuncionObjetivo
    global restricciones

    #archivoSalida = "solucionSimplexDual"
    #file = Archivo(archivoSalida)

    asignarElementos(elementosEntrada)

    global numeroVariablesDecision

    controlador = Controlador(tipoDeOptimizacion,coeficientesFuncionObjetivo,restricciones,int(numeroVariablesDecision),file, True)
    controlador.inicioControlador()
    float
#Funcion que se encarga de llamar a las distintas funciones para hacer validaciones del archivo de entrada
def asignarElementos(elementosEntrada):
    validarTipoOptimizacion(elementosEntrada[0])
    validarNumeroArgumentos(elementosEntrada[1])
    validarCoeficientesFuncionObjetivo(elementosEntrada[2])
    validarRestricciones(elementosEntrada)

#Valida si el tipo de optimizacion es min o max
#Retorna a la funcion anterior (asignarElementos)
def validarTipoOptimizacion(optimizacion):
    global tipoDeOptimizacion
    if optimizacion == "min" or optimizacion == "max":
        if optimizacion == "min":
            tipoDeOptimizacion = True
            #print("El tipo de optimizacion es: " + tipoDeOptimizacion)
            return
        else:
            tipoDeOptimizacion = False
    else:
        print("ERROR: Tipo de optimizacion incorrecto")
        print("Usted ingreso : " + str(optimizacion))
        print("Esperaba : min o max")
        exit(0)

#Valida si la cantidad de argumentos ingresados son unicamento dos (decision,argumentos)
#Retorna a la funcion anterior(asignarElementos)
def validarNumeroArgumentos(linea2Archivo):
    global numeroRestricciones
    global numeroVariablesDecision
    #Separa por , o espacio en blanco
    numeroArgumentos = len(re.split(",| ",linea2Archivo))
    if numeroArgumentos == 2:
        numeroVariablesDecision,numeroRestricciones = linea2Archivo.split(",")
        #Valida si lo ingresado son numeros enteros
        try:
            val = int(numeroVariablesDecision)
            val2 = int(numeroRestricciones)
        except ValueError:
            print("ERROR: Alguno de los valores ingresados no es un entero")
            exit(0)
        #print("El numero de numeroVariablesDecision es : " + numeroVariablesDecision)
        #print("El numero de numeroRestricciones es : " + numeroRestricciones)
        return
    else:
        print("ERROR: Se pasa de argumentos en la linea 2 del archivo")
        print("Usted ingreso : " + str(numeroArgumentos))
        print("Se esperan 2 argumentos : Variables de Decision, Restricciones")
        exit(0)

#Valida si los coeficientes ingresados son igual a la cantidad de variables de Decision
#Retorn a la funcion anterior (asignarElementos)
def validarCoeficientesFuncionObjetivo(linea3Archivo):
    global numeroVariablesDecision
    global coeficientesFuncionObjetivo
    numeroArgumentos = len(re.split(",",linea3Archivo))
    args = re.split(",",linea3Archivo)
    i = 0
    #Si el numero de argumentos es igual al numero de variables de decision
    if(int(numeroArgumentos) == int(numeroVariablesDecision)):
        #For para recorrer cada uno de los argumentos, validar si son enteros y guardarlos en la lista de coeficientesFuncionObjetivo
        for i in range(int(numeroVariablesDecision)):
            try:
                val = float(args[i])
            except ValueError:
                print("ERROR: Alguno de los valores ingresados no es un entero")
                exit(0)
            coeficientesFuncionObjetivo.append(float(args[i]))
    else:
        print("ERROR: El numero de coeficientes de la funcion objetivo es distinto al numero de variables de decision")
        print("Usted ingreso : " + str(numeroArgumentos))
        print("Se esperaban : " + str(numeroVariablesDecision))
        exit(0)
    return

#Valida si las restricciones cumplen con lo siguiente:
## Validacion 1: El numero de restricciones es igual a la cantidad que se ingresado
##Validacion 2: Cada restriccion tiene unicamente numeros enteros y termina con <=,>= o =
##Validacion 3: La restriccion tenga el mismo numero de coeficientes que el numero de variables de descision + 1
def validarRestricciones(listaDeElementos):
    global numeroRestricciones
    global restricciones
    global numeroVariablesDecision
    #Validacion 1
    if (len(listaDeElementos)-3) == int(numeroRestricciones):
        #Apartir de 3 estan las restricciones
        for k in range(3,len(listaDeElementos)):
            #Agarra cada restriccion y separa los elementos por cada ,
            listaAux = listaDeElementos[k]
            args = re.split(",",listaAux)
            #Validacion 3
            if (len(args)-1) != (int(numeroVariablesDecision) + 1):
                print("ERROR: Alguna restriccion se encuentra incomplete o el numero de variables de decision ingresada es incorrecto")
                exit(0)
            for i in range((len(args)-1) ):
                try:
                    val = float(args[i])
                    args[i] = float(args[i])
                except ValueError:
                    print("ERROR: Alguno de los valores ingresados no es un entero")
                    exit(0)
            #Validacion 2
            if(args[-1] == "=" or args[-1] == "<=" or args[-1] == ">="):
                restricciones.append(args)
            else:
                print("ERROR: Alguna de las restricciones no cumple con ser =, <= o >=")
                print("Usted ingreso : " + str(args[-1]))
                print("Se esperaba: =, <=, o >=")
                exit(0)
    else:
        print("ERROR: Numero de restricciones diferente a la cantidad ingresada")
        print("Usted ingreso : " + str((len(listaDeElementos)-3)))
        print("Se esperaban : " + str(numeroRestricciones))
        exit(0)
    return

#INICIO DEL PROGRAMA
#main()
