from Principal import *

matrizTrans = [] #matriz a usar como transpuesta
matrizNueva = [] #matriz que se va usar para agregar las de holgura y artificial 
listaZFase1 = [] #lista donde se guarda el resultado de Z con las variables agregadas 
listaNueva = []
Resultado = []  #lista donde se guardan el resultado antes de agregar las variables de holgura y artificial en max
ResultadoMin = [] #lista donde se guardan el resultado antes de agregar las variables de holgura y artificial en min
masHolgura=0 #variable para llevar un contador de cuantas variables de holgura positivas se debe agregar 
menosHolgura=0 #variable para llevar un contador de cuantas variables de holgura negativas se debe agregar
artificial=0 #variable para llevar un contador de cuantas variables de artificial se debe agregar


#funcion que crea la matriz transpuesta vacia a partir del numero de variables y restricciones    
def crearMatrizTrans(variables, restricciones):
    #Creacion de una matriz vacia
    for i in range(variables):
        matrizTrans.append([])
        for j in range(restricciones+2):
            matrizTrans[i].append(None)
     ###################################     

#Agarra la funcion objetivo y cada una de las restricciones y le agrega las de holgura y artificial que llevan cada una 
def agregarHA(variables,restricciones):
    global menosHolgura
    global masHolgura
    global artificial
    #agrega la fila de Z mas las variables de holgura y artificiales 
    for i in range(restricciones):
        listaZFase1.append(listaNueva[i])
    for j in range(masHolgura):
        listaZFase1.append(0)#agrega 0 porque las de holgura llevan 0 
    for i in range(menosHolgura):
        listaZFase1.append(0)#agrega 0 porque las de holgura llevan 0 
    for y in range(artificial):
        listaZFase1.append(-1)#agrega -1 porque las artificiales en Z llevan -1 al pasar del otro lado 
    listaZFase1.append(0)
    matrizNueva.append(listaZFase1)#Anade esa lista a la matriz que se va imprimir 

    #agrega cada restriccion en una lista con las variables de holgut=ra y artificial en 0 y las mete a la matriz
    for i in range(variables):
        listaRestriccion = []
        for j in range(restricciones):
            listaRestriccion.append(int(matrizTrans[i][j]))
        for x in range(menosHolgura):
            listaRestriccion.append(0)
        for x in range(masHolgura):
            listaRestriccion.append(0)
        for x in range(artificial):
            listaRestriccion.append(0)
        listaRestriccion.append(int(matrizTrans[i][restricciones]))
        listaRestriccion.append(matrizTrans[i][restricciones+1])
        matrizNueva.append(listaRestriccion)

    #agregar los 1 de holgura y artificial
    for i in range(menosHolgura):
        matrizNueva[i+1][restricciones+i]=-1
    for i in range(masHolgura):
        matrizNueva[i+1][restricciones+menosHolgura+i]=1
    for i in range(artificial):
        matrizNueva[i+1][restricciones+menosHolgura+masHolgura+i]=1
    #print(matrizNueva)

#Lleva los contadores de la cantidad de variables que se deben agregar y sino hay imprime que no hay signos 
def evaluarRestricciones(restricciones, variables):
    global menosHolgura
    global masHolgura
    global artificial
    for i in range(variables):
        if(matrizTrans[i][restricciones+1] == ">="):
            artificial = artificial +1
            menosHolgura = menosHolgura +1
        elif(matrizTrans[i][restricciones+1] == "<="):
            masHolgura = masHolgura +1
        elif(matrizTrans[i][restricciones+1] == "="):
            artificial = artificial +1
            #print("igual")
        else:
            print("No hay signos")
    
########################################################################]
#MAX
#Funcion de max que recibe las variables, restricciones, listaVariables que es la que contiene la fila de Z
# y tambien matrizX que es la que nos manda la interfaz 
def dualMax(variables, restricciones,matrizX, listaVariables, file):
    file.write("Funcion Max objetivo entrante\n")
    print("Funcion Max objetivo entrante")
    file.write(str(listaVariables)+"\n")
    print(listaVariables)
    file.write("Restricciones entrantes\n")
    print("Restricciones entrantes")
    print(matrizX)
    file.write(str(matrizX)+"\n")
    file.write("Variables entrantes\n")
    print("Variables entrantes")
    file.write(str(variables)+"\n")
    print(variables)
    file.write("Restricciones entrantes\n")
    print("Restricciones entrantes")
    file.write(str(restricciones)+"\n")
    print(restricciones)
    print("-----------------------------------------------------")
    file.write("-----------------------------------------------------\n")

    #Aqui debo recibir el signo dada por la interfaz 
    signo = ">="#input()
    file.write("Signo de no negatividad\n")
    file.write(str(signo)+"\n")
    file.write("-----------------------------------------------------\n")
        
    #transpuesta
    #listaNueva contiene la nueva Min W
    for x in range(0,restricciones):
        listaNueva.append(matrizX[x][variables])#Le asigno a listaNueva los nuevos valores de Z
    #print(listaNueva)

    #Con este for se tranpone la matriz con los datos de Z que estaban en listaVariables 
    for x in range(variables):
        matrizTrans[x][restricciones]=listaVariables[x]
        matrizTrans[x][restricciones+1]=signo

    #Con este for transpone la matrizX en la matrizTrans que sera la que vamos a utilizar 
    for w in range(variables):
        for y in range(restricciones):
            matrizTrans[w][y]=matrizX[y][w]       
    
    
    #Agregando al resultado para en un futuro mandarlo a la funcion simplex 
    Resultado.append("min")
    Resultado.append(str(restricciones)+","+str(variables))
    ###################################################################
    #Este for lo que hace es agarrar cada elemento en listaNueva que es el Z nuevo y lo mete en resultado 
    var=""
    for i in range(0,len(listaNueva)):
        var = var + listaNueva[i]
        if(i<len(listaNueva)-1):
            var = var + ","
    Resultado.append(var)

    ####################################################################
    #Agarra cada restriccion de la matriz y la va anadiendo al resultado como una lista de string 
    for i in range(variables):
        var=""
        for y in range(restricciones+2):
            var = var + matrizTrans[i][y]
            if(y<restricciones+1):
                var = var + ","
        Resultado.append(var)
    #Impresiones finales
    file.write("-----------------------------------------------------\n")
    file.write("Resultado Dual\n")
    print("RESULTADO DUAL")
    #print(Resultado)#Aca se puede ver el Resultado que puede ser enviado a una funcion nueva 
    file.write("Funcion objetivo saliente\n")
    print("Funcion objetivo saliente")
    file.write(str(listaNueva)+"\n")
    print(listaNueva)
    file.write("Restricciones salientes\n")
    print("Restricciones salientes")
    file.write(str(matrizTrans)+"\n")
    print(matrizTrans)
    file.write("Numero de variables salientes\n")
    print("Numero de variables salientes")
    file.write(str(restricciones)+"\n")
    print(restricciones)
    file.write("Numero de restricciones salientes\n")
    print("Numero de restricciones salientes")
    file.write(str(variables)+"\n")
    print(variables)
    evaluarRestricciones(restricciones, variables)#Funcion oara evaluar las restricciones y sumas las variables 
    agregarHA(variables,restricciones)#Funcion que agrega las variables a cada fila 
    z=int(menosHolgura)+int(masHolgura)
    i = int(artificial)
    file.write("Matriz final con variables agregadas\n")
    print("Matriz final con variables agregadas")
    file.write("Se agregaron "+str(z)+" variables de holgura\n")
    print("Se agregaron "+str(z)+" variables de holgura")
    file.write("Se agregaron "+str(i)+" variables artificiales\n")
    print("Se agregaron "+str(i)+" variables artificiales")
    #imprimir matriz en forma ordenada
    for y in range(variables+1):
        if(y==0):
            file.write("Z: " + str(matrizNueva[y])+"\n")
            print("Z: " + str(matrizNueva[y]))
        else:
            file.write("R: " + str(matrizNueva[y])+"\n")
            print("R: " + str(matrizNueva[y]))
    #print(matrizNueva)
    print("Resultado enviado a funcion de simplex")
    file.write("Resultado enviado a funcion de simplex\n")
    file.write(str(Resultado)+"\n")

    #print(Resultado)
    mainDual(Resultado, file)
    #print(Resultado)
    
    

#########################################################################
#MIN
#Funcion de min que recibe las variables, restricciones, listaVariables que es la que contiene la fila de Z
# y tambien matrizX que es la que nos manda la interfaz 
def dualMin(variables, restricciones,matrizX, listaVariables, file):
    file.write("Funcion Min objetivo entrante\n")
    print("Funcion Min objetivo entrante")
    file.write(str(listaVariables)+"\n")
    print(listaVariables)
    file.write("Restricciones entrantes\n")
    print("Restricciones entrantes")
    print(matrizX)
    file.write(str(matrizX)+"\n")
    file.write("Variables entrantes\n")
    print("Variables entrantes")
    file.write(str(variables)+"\n")
    print(variables)
    file.write("Restricciones entrantes\n")
    print("Restricciones entrantes")
    file.write(str(restricciones)+"\n")
    print(restricciones)
    print("-----------------------------------------------------")
    file.write("-----------------------------------------------------\n")
    
    #Aqui debo recibir el signo dado por la interfaz 
    signo = ">="#input()
    file.write("Signo de no negatividad\n")
    file.write(str(signo)+"\n")
    file.write("-----------------------------------------------------\n")
        
    #transpuesta
    #listaNueva contiene la nueva Min W
    for x in range(restricciones):
        listaNueva.append(matrizX[x][variables])#Le asigno a listaNueva los nuevos valores de Z
        #print(listaNueva)

    
    #Con este for transpone la matrizX en la matrizTrans que sera la que vamos a utilizar 
    for w in range(variables):
        for y in range(restricciones):
            matrizTrans[w][y]=matrizX[y][w]       

    #Con este for se tranpone la matriz con los datos de Z que estaban en listaVariables y depende de signo lo cambia ya que es la funcion de MIN
    for x in range(variables):
        matrizTrans[x][restricciones]=listaVariables[x]
        if(signo == '>='):
            matrizTrans[x][restricciones+1]= "<="
        elif(signo == '<='):
            matrizTrans[x][restricciones+1]= ">="
        else:
            matrizTrans[x][restricciones+1]= "="
    #Agregando al resultado
    ResultadoMin.append("max")
    ResultadoMin.append(str(restricciones)+","+str(variables))
    ###################################################################
    var=""
    for i in range(0,len(listaNueva)):
        var = var + listaNueva[i]
        if(i<len(listaNueva)-1):
            var = var + ","
    ResultadoMin.append(var)

    ####################################################################
    
    for i in range(variables):
        var=""
        for y in range(restricciones+2):
            var = var + matrizTrans[i][y]
            if(y<restricciones+1):
                var = var + ","
        ResultadoMin.append(var)
    file.write("-----------------------------------------------------\n")
    file.write("Resultado Dual\n")
    print("RESULTADO DUAL")
    file.write("Funcion objetivo saliente\n")
    print("Funcion objetivo saliente")
    print(listaNueva)
    file.write("Restricciones salientes\n")
    print("Restricciones salientes")
    print(matrizTrans)
    file.write("Numero de variables salientes\n")
    print("Numero de variables salientes")
    print(restricciones)
    file.write("Numero de restricciones salientes\n")
    print("Numero de restricciones salientes")
    print(variables)
    evaluarRestricciones(restricciones, variables)
    agregarHA(variables,restricciones)
    z=int(menosHolgura)+int(masHolgura)
    i = int(artificial)
    file.write("Matriz final con variables agregadas\n")
    print("Matriz final con variables agregadas")
    file.write("Se agregaron: "+str(z)+" variables de holgura\n")
    print("Se agregaron: "+str(z)+" variables de holgura")
    file.write("Se agregaron: "+str(i)+" variables artificiales\n")
    print("Se agregaron: "+str(i)+" variables artificiales")
    #imprimir matriz en forma ordenada
    for y in range(variables+1):
        if(y==0):
            file.write("Z: " + str(matrizNueva[y])+"\n")
            print("Z: " + str(matrizNueva[y]))
        else:
            file.write("R: " + str(matrizNueva[y])+"\n")
            print("R: " + str(matrizNueva[y]))
    #print(matrizNueva)
    print("Resultado enviado a funcion de simplex")
    file.write("Resultado enviado a funcion de simplex\n")
    file.write(str(Resultado)+"\n")
    
    #print(ResultadoMin)
    mainDual(ResultadoMin, file)
    #print(ResultadoMin)
