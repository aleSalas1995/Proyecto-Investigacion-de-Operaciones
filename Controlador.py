import copy
from MetodoSimplex import*
tabla=[[]]
variablesDecision=0
arregloCol=[]
arregloFilas=["Z"]
arregloZ=[]
arregloZ2=[]
#-----------------------------------------------------------
class Z_Aux:
    #Constructor
    '''
    Clase en la cual se cuenta con un constructor encargado de 
    crear un objeto el cual tiene como atributo numero y letra valor 
    la cual hace referencia a la columna en que se ubique
    '''
    def __init__(self,NUM,letra):
      
        self.NUM=NUM
        self.letra=letra 
#-----------------------------------------------------------
#crear Z
class Z:
    #Constructor
    '''
    Clase la cual recibe como parametro si se trata de minimizar o 
    maximizar, ademas de una lista de lista en la cual se encuentran
    las restricciones en formato de [[3,2,1,"<="]] en donde los numeros
    corresponden a float o int y el simbolo es un string

    '''
    def __init__(self,arreglo,esMin,u):
        self.esMin= esMin
        self.restricciones=arreglo
        self.u= u


    '''
    Funcion en la cual se crean los objetos
    correspondientes a las variables basicas
    con sus respectivos atributos del numero y
    letra ya sea x1 x2 etc
    Ademas se agrega la solucion identificada mediante SOL
    '''    
    def crearZ(self):
        global tabla
        self.convertirNulo_ObjetosU()
        for i in range(len(self.u)):
            global arregloZ
            if self.esMin == True:
                z=Z_Aux(self.u[i]*-1,"x"+str(i+1))
            else:
                z=Z_Aux(self.u[i],"x"+str(i+1))
            arregloZ.append(z)
        sol=Z_Aux(0,"SOL")
        arregloZ.append(sol)


    ''' 
    Funcion en la cual se verifica si la variable
    se encuentra en el arreglo  para ello se utiliza 
    la letra que lo ubica en la columna
    '''
    def buscarArreglo(self,identificador):
        global arregloZ
        for x in range(len(arregloZ)):
            if arregloZ[x].letra == identificador:
                return x
        return -1

    '''
    Funcion que verifica si se trata de minimizar o 
    maximizar , en caso de que sea minimizar cambiara de
    signo al numero debido al despeje que se debe hacer
    al colocar Z

    '''
    def verificarMinX(self,numero):
        if self.esMin is True:
            #print(numero*-1)
            return numero*-1
        else: return numero
       
    '''
    Funcion la cual va agregando va recorriendo restriccion por restriccion
    para realizar la suma correspondiente de acuerdo al despeje
    de las variables artificiales con los valores de la funcion objetivo
    '''
    def agregarRestricciones(self):
        global arregloZ
        for i in range (len(self.restricciones)):
     
            if self.restricciones[i][len(self.restricciones[i])-1]!= "<=":
                for j in range(len(self.restricciones[i])-2): ## por que los dos ultimos son solucion y simbolo
                    if self.buscarArreglo("x"+str(j+1)) != -1: # si lo encontro devuelve la pos donde esta si no -1
                        numero = self.verificarMinX(self.restricciones[i][j])# si es minimizar lo deja igual

                numero = self.verificarMinX(self.restricciones[i][len(self.restricciones[i])-2])# si es minimizar lo multiplica*-1
                x=self.buscarArreglo("SOL")
                 
            self.cambiarSignos()


    '''
    Funcion que cambia el signo del numero en la fila Z
    '''
    def cambiarSignos(self):
        global arregloZ,tabla
        #if self.esMin is not True:
        arregloZ[len(arregloZ)-1].NUM=arregloZ[len(arregloZ)-1].NUM*-1
        #print("Prueba "+str(arregloZ[len(arregloZ)-1].NUM))

        for x in range(len(arregloZ)):
            tabla[0][self.ubicar_En_Tabla(arregloZ[x])]=arregloZ[x]    

    '''
    Funcion la cual se utiliza para ubicar en la tabla
    el elemento de la fila U
    '''
    def ubicar_En_Tabla(self,elemento):
        global arregloCol
        for x in range(len(arregloCol)):
            if elemento.letra == arregloCol[x]:
                return x
        return -1         

    ''' 
    Funcion que se utliza para 
    la creacion de objetos pertenecientes a las 
    variables de holgura en donde el valor del numero 
    corresponde a 0 0
    '''
    def convertirNulo_ObjetosU(self):
        for x in range(len(arregloCol)):
            z=Z_Aux(0,arregloCol[x])
            tabla[0][x]=z
       

#-------------------------------------------------------
#Matriz     

class Matriz:
    #Constructor
    def __init__(self, arreglo):
        self.matriz = arreglo
       
    def set_Matriz(self, valor):  #set matriz  
        print("Matriz cambiada")
        self.matriz = valor

    def get_Matriz(self): #get de la matriz 
        return self.matriz

    '''
    Funcion en la cual se crea la matriz a utilizar
    contando las variables artificiales, holgura y basicas
    en caso de tenerlas
    Ademas se agregan dos columnas extra para colocar
    la solucion y el resultado de la division para
    la seleccion del fila pivot
    '''
    def cantidad_filas(self):
        if(len(self.matriz) is not 0):
           global variablesDecision, tabla
           filas=variablesDecision+2 # col solucion y col division
           for i in range (len(self.matriz)):
               indica = self.matriz[i][len(self.matriz[i])-1]
               filas+=self.cantidad_filasAux(indica)
        tabla=[[0 for i in range(filas)] for i in range(len(self.matriz)+1)]

    def cantidad_filasAux(self,argument): # verifica si va necesitar el espacio para R y -S
        switcher = {">=": 2}
        return switcher.get(argument, 1)

    def variablesX(self):
        global variablesDecision
        for i in range (0,variablesDecision):
            arregloCol.append("x"+str(i+1))

#-----------------------------------------------------------
#Restricciones

class Restricciones:
    #Constructor
    def __init__(self, arreglo,esMin):
        self.matriz = arreglo
        self.varR=1
        self.varS=1
        self.esMin=esMin
    '''
    Funcion en la cual se colococan dentro de la tabla general a utilizar
    un 1 0 -1 a las variables correspondientes a las artificiales
    '''   
    def colocar_Restricciones(self):
        global variablesDecision
        posicion = variablesDecision-1  # aumenta en R y S
        
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])-2):
                tabla[i+1][j]=self.matriz[i][j]
            m = Matriz(self.matriz)
            self.verificar_Signo(self.matriz[i][len(self.matriz[i])-1])
            x= m.cantidad_filasAux(self.matriz[i][len(self.matriz[i])-1])
            posicion += x
            tabla[i+1][len(tabla[i])-2]=self.matriz[i][len(self.matriz[i])-2]
            if x is 2:
                tabla[i+1][posicion-1]=1
                tabla[i+1][posicion]=-1
            else: tabla[i+1][posicion]=1
        '''
        como se menciono anteriormente
        se agregan dos columnas extras
        que corresponden a la solucin y a una
        para la division
        '''    
        arregloCol.append("SOL")
        arregloCol.append("DIV")

    '''
    Funcion en la cual se agrega al arreglo que muestra las filas
    y las columnas una R representando variable artificial
    y una S en caso de ser una variable de holgura
    Se le adiciona el nuemero para poder diferenciarlas
    '''   
    def MayorIgual(self):
        arregloCol.append("R"+str(self.varR))
        arregloCol.append("S"+str(self.varS))
        arregloFilas.append("R"+str(self.varR))
        z=Z_Aux(0,"S"+str(self.varS))
        global arregloZ
        arregloZ.append(z)
        self.varR+=1
        self.varS+=1
        
    def verificar_Min(self,argument):#verifica que se trate de minimizar o maximizar 
        switcher = {True: 1}
        return switcher.get(argument, -1)
            
    '''
    Funcion la cual agrega una S asemejando a una variable
    holgura tanto al arreglo de filas como el arreglo 
    de columnas , es cuando se recibe un signo <=
    '''
    def MenorIgual(self):
        arregloCol.append("S"+str(self.varS))
        arregloFilas.append("S"+str(self.varS))
        self.varS+=1

    '''
    Funcion en la que se agrega una R asimilando 
    una variable artificial, se agrega cuando 
    en la restriccion el signo es un =, se anade 
    al arreglo de filas y columnas
    '''
    def Igual(self):
        arregloCol.append("R"+str(self.varR))
        arregloFilas.append("R"+str(self.varR))
        self.varR+=1    
 
    def verificar_Signo(self,signo): # verifica cual signo corresponde a la restriccion
        switcher = {">=": self.MayorIgual,"<=": self.MenorIgual, "=": self.Igual }
        switcher [signo]()
        

#------------------------------------------------------------          
class Controlador:
    '''
    Metodo main en donde se llaman a las funciones para
    la implementacion del metodo simplex
    '''
    def __init__(self,minimo,U,restricciones,vars,file,esDual):
        global variablesDecision

        self.esDual=esDual

        self.archivo=file
        #print(U)
        variablesDecision=vars
        self.esMinimizar= minimo# se recibe
        #print("Es minimizar "+str(self.esMinimizar))
        self.arregloZ=U
        #print("arregloZ "+str(self.arregloZ))
        self.arregloEntrada=restricciones
        #print("arregloEntrada "+str(self.arregloEntrada)) 

    '''
    Funcion en la cual se controla la creacion del areglo con objetos
    pertenecientes a la fila U, ademas se crea la tabla de forma estandarizada
    '''
    def inicioControlador(self):    
        print("\n * R = Var Artificial    \n * S = Var Holgura       \n * X = Var Decision      \n\n")
        self.archivo.write("\n * R = Var Artificial    \n * S = Var Holgura       \n * X = Var Decision      \n\n")
        dosFases = False
        for i in range(len(self.arregloEntrada)):
            if self.arregloEntrada[i][-1] != "<=":
                dosFases = True
                break

        matriz = Matriz(self.arregloEntrada) # crea objeto para la impresion
        matriz.cantidad_filas() # crea la tabla
        matriz.variablesX()
        restricciones=Restricciones(self.arregloEntrada,self.esMinimizar)
        restricciones.colocar_Restricciones()
        
        z=Z(self.arregloEntrada,self.esMinimizar,self.arregloZ)
        z.crearZ()
        z.agregarRestricciones()

        global arregloFilas,arregloCol,tabla

        if self.esDual == True:

            print("\nMetodo Dual\n")
            MS=MetodoSimplex(tabla,arregloFilas,arregloCol,self.esMinimizar,self.archivo)
            matrizDual = MS.start_MetodoSimplex_Max()
            arregloDual = self.imprimirResultadoDual(matrizDual)
            print("\nSoluciones del problema original\n")
            self.archivo.write("\nSoluciones del problema original\n")
            for i in range(len(arregloDual)):
                self.archivo.write("X"+str(i+1)+" = "+str(arregloDual[i])+"\n")
                print("X"+str(i+1)+" = "+str(arregloDual[i]))

        else:

            if dosFases == False:
                MS=MetodoSimplex(tabla,arregloFilas,arregloCol,self.esMinimizar,self.archivo)
                MS.start_MetodoSimplex_Max()

            else:

                ##Fase1##

                print("\n** Metodo dos fases **\n")
                print("\n-> Fase #1\n")

                nuevoN = self.generarNuevoN()
                nuevaTabla = self.generarTablaF1(nuevoN)

                MS=MetodoSimplex(nuevaTabla,arregloFilas,arregloCol,self.esMinimizar,self.archivo)
                MatrizF1 = MS.start_MetodoSimplex_Max()

                print("\nFase 1 Lista\n")
                
                ##Fase2##
                print("\n->Fase #2\n")

                #print(MatrizF1)
                self.generarTablaF2(MatrizF1)
                nuevaTabla = self.eliminarVariablesArtificiales()    
                nuevoArregloCol = self.actualizarArregloCol()
                nuevaTablaConCeros = self.hacerCeros(nuevaTabla,arregloFilas, nuevoArregloCol)            

                MS=MetodoSimplex(nuevaTabla,arregloFilas,nuevoArregloCol,self.esMinimizar,self.archivo)
                MatrizF1 = MS.start_MetodoSimplex_Max()
                #print(MatrizF1)
                print("Fase 2 Lista")
    
    def imprimirResultadoDual(self, matrizDual):
        arregloDual =  []
        for i in range(len(matrizDual[0])):

            if matrizDual[0][i].letra !=  "SOL":
                if "S" in matrizDual[0][i].letra:
                    arregloDual.append((round(matrizDual[0][i].NUM*-1,2)))
        return arregloDual



    def hacerCeros(self, nuevaTabla, arregloFilas, nuevoArregloCol):

        for i in range(len(nuevoArregloCol)):
            for j in range(len(arregloFilas)):
                
                if arregloFilas[j] == nuevoArregloCol[i]:
                    #print("if "+str(arregloFilas[j])+">"+str(j)+"--"+str(nuevoArregloCol[i])+">"+str(i))
                    #print("prueba  "+str(nuevaTabla[j][i]))
                    nuevaTabla = self.modificar_FilaZ(j,i, nuevaTabla)
                    #return nuevaTabla
                #print(nuevoArregloCol[j])
        return nuevaTabla

    def modificar_FilaZ(self,filaPivot,columnaPivot,nuevaTabla):
        
        lista=[]
        lista2=[]
        for i in range(len(nuevaTabla[0])-2):
            #print("columna pivot "+str(columnaPivot))
            arg2=nuevaTabla[0][columnaPivot].NUM
            #print(nuevaTabla[0][i].letra)
            #print("arg2=tabla[0][columnaPivot].NUM")
            #print(arg2)

            y=nuevaTabla[0][i].NUM-arg2*nuevaTabla[filaPivot][i]
            #print("tabla[0][i].NUM")
            #print(nuevaTabla[0][i].NUM)
            #print("tabla[filaPivot][i]")
            #print(nuevaTabla[filaPivot][i])

            #print("y")
            #print(y)
            lista2.append(y)
            
        #print(lista)
        arg2=nuevaTabla[0][columnaPivot].NUM
        #print("arg2 v2")
        #print(arg2)
        if self.esMinimizar is True:
            y=nuevaTabla[0][len(nuevaTabla[0])-2].NUM-arg2*nuevaTabla[filaPivot][len(nuevaTabla[0])-2]
            #print("y v2")
            #print(y)
        else:
            y=nuevaTabla[0][len(nuevaTabla[0])-2].NUM+arg2*nuevaTabla[filaPivot][len(nuevaTabla[0])-2]
        lista2.append(y)
        x=0
        while x < len(lista2):
            nuevaTabla[0][x].NUM=lista2[x]
            x+=1
        #print("-------------------")
        #print(lista2)
        return nuevaTabla
    ''' 
    Funcion encargada de colocar el nuevo U para realizar la primera fase
    '''
    def generarTablaF1(self,nuevoN):

        global tabla
        tablaAux = copy.deepcopy(tabla)
        nuevoZ = []

        x = 0
        for i in range(len(tablaAux[0])):
            x = nuevoN[i] + x
            for j in range(len(tablaAux)):
                if j != 0:
                    x = tablaAux[j][i] + x
            #if self.esMinimizar == False:
            #    nuevoZ.append(x)
            #else: 
            #    nuevoZ.append(x*-1)
            nuevoZ.append(x)
            x = 0

        #Generar nueva tabla
        for i in range(len(tablaAux[0])):
            tablaAux[0][i].NUM = nuevoZ[i]

        return tablaAux

    '''
    Crea una fila de 0 y -1(si es artificial), para realizar 
    la suma de columnas y poder calcular el U de la primera Fase
    '''
    def generarNuevoN(self):       

        arreglo = []
        for i in range(len(tabla[0])):
            if 'R' in tabla[0][i].letra:
                arreglo.append(-1)
            else:
                arreglo.append(0)
        
        return arreglo

    '''
    Coloca el U original en la matriz, con las filas (restricciones)
    de la fase #1
    '''
    def generarTablaF2(self, MatrizF1):
        global tabla
        for i in range(len(tabla)):
            if i > 0:
                #print("tabla[i] "+str(tabla[i]))
                #print("MatrizF1[i] "+str(MatrizF1))
                tabla[i] = MatrizF1[i]
        #for i in range(len(tabla[0])):
            #if self.esMinimizar == False:
                #tabla[0][i].NUM = tabla[0][i].NUM
            #else:
                #if "SOL" not in tabla[0][i].letra: 
                #tabla[0][i].NUM = tabla[0][i].NUM*-1 

    '''
    Elmina las columnas con variables artificiales
    '''
    def eliminarVariablesArtificiales(self):
        global tabla 

        tablaF2 = []
        arregloF2 = []

        for i in range(len(tabla)):
            for j in range(len(tabla[0])):
                if 'R' not in tabla[0][j].letra:
                    arregloF2.append(tabla[i][j])

            tablaF2.append(arregloF2)
            arregloF2 = []

        return tablaF2

    '''
    Elimina las R de el arreglo que contiene los identificadores 
    de cada columna
    '''
    def actualizarArregloCol(self):
        global arregloCol
        nuevoArregloCol = []
        for i in range(len(arregloCol)):
            if 'R' not in arregloCol[i]:
                nuevoArregloCol.append(arregloCol[i])
        return nuevoArregloCol


