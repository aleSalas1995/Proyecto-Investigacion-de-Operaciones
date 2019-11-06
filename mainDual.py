from tkinter import *
from Dual import *
from Imprimir import*

listaCambiada = []
matrizX = []
listaVariables=[]


##############################################
def modificar(variables,restricciones,decision):

    archivoSalida = "solucionDual"
    file = Archivo(archivoSalida)

    crearMatrizTrans(variables, restricciones)
    lista=[]
    for x in range(variables):
            listaVariables.append(listaCambiada[x])


    for y in range(variables, len(listaCambiada)):
            #for j in range(variables+1):
            lista.append(listaCambiada[y])


    filas=variables+2
    matrizX = [lista[filas*i : filas*(i+1)] for i in range(restricciones)]



    if(decision.get() == "Máximo"):
            dualMax(variables,restricciones,matrizX, listaVariables,file.getArchivo())
    else:
            dualMin(variables,restricciones,matrizX, listaVariables,file.getArchivo())



class matrizDatos:


    def __init__(self, master):

        frame = Frame(master)
        frame.pack(side=TOP)
        #-----------------------------------------------------------------------------
        minMax = ["Máximo","Mínimo"]
        self.opcion = StringVar()
        self.opcion.set(minMax[0])
        self.titulo = Label(frame,text="Escoja Máximo o Mínimo:")
        self.titulo.grid(row=0,sticky=W)
        self.menuOpciones = OptionMenu(frame,self.opcion,*minMax)
        self.menuOpciones.grid(row=0,column=1)
        #-----------------------------------------------------------------------------
        self.space = Label(frame,text=" ")
        self.space.grid(row=2,sticky=W)

        self.varLab = Label(frame,text="Variables")
        self.varLab.grid(row=3,sticky=W)
        self.variables = Spinbox(frame,from_=2, to=5,state="readonly",width=10)
        self.variables.grid(row=4,sticky=W)
        #-----------------------------------------------------------------------------
        self.resLab = Label(frame,text="Restricciones")
        self.resLab.grid(row=5,sticky=W)
        self.restricciones = Spinbox(frame,from_=2, to=5,state="readonly",width=10)
        self.restricciones.grid(row=6,sticky=W)
        #-----------------------------------------------------------------------------

        lin = Label(frame,text="")
        lin.grid(row=7,sticky=W)

        self.button = Button(frame,text="Aceptar", relief = RAISED,command = lambda:self.funcionObjetivo(master,self.opcion,self.variables,self.restricciones,self.button))
        self.button.grid(row=8,sticky=W)


    def funcionObjetivo(self,master,opcion,variables,restricciones,boton):
        boton.destroy()
        vas = int(variables.get())
        res = int(restricciones.get())
        frame2 = Frame(master)
        frame2.pack(side=TOP)
        columCount = 0
        func = Label(frame2,text=opcion.get()+" = ")
        func.grid(row=0,column=columCount)
        columCount+=1

        funcEspacios = []
        funcEspacios.append([])
        for i in range(0,vas):

            cuadrito = Entry(frame2,width=5,relief=RAISED)
            funcEspacios[0].append(cuadrito)       #necesito control de cuadritos
            cuadrito.grid(row=0,column=columCount)
            columCount+=1

            x = "x"+str(i+1)
            xpos = Label(frame2,text=x)
            xpos.grid(row=0,column=columCount)
            columCount+=1

            if i+1!=vas:
                suma = Label(frame2,text=" + ")
                suma.grid(row=0,column=columCount)
                columCount+=1


        lin = Label(frame2,text="")
        lin.grid(row=9,sticky=W)

        self.buttonx = Button(frame2,text="Aceptar", relief = RAISED,command = lambda:self.restriccionesLlenar(master,self.opcion,vas,res,funcEspacios,self.buttonx))
        self.buttonx.grid(row=10,sticky=W)

        # self.button2 = Button(frame2,text="Aceptar", relief = RAISED,command = lambda:self.matriciar(master,self.opcion,vas,res,funcEspacios,self.button2))
        # self.button2.grid(row=10,sticky=W)
        #self.hola(master,opcion,variables,restricciones)

    def restriccionesLlenar(self,master,opcion,variables,restricciones,funcEspacios,buttonx):
        buttonx.destroy()
        for p in funcEspacios:
            for q in p:
                q.config(state="readonly")
        frame4 = Frame(master)
        frame4.pack()


        for i in range(0,restricciones):
            columCount=0
            funcEspacios.append([])
            for y in range(0,variables):
                cuadrito = Entry(frame4,width=5,relief=RAISED)
                funcEspacios[i+1].append(cuadrito)       #necesito control de cuadritos
                cuadrito.grid(row=i,column=columCount)
                columCount+=1

                x = "x"+str(y+1)
                xpos = Label(frame4,text=x)
                xpos.grid(row=i,column=columCount)
                columCount+=1

                if y+1!=variables:
                    suma = Label(frame4,text=" + ")
                    suma.grid(row=i,column=columCount)
                    columCount+=1

            simbolo = [">=","<=","="]
            simb = StringVar()
            simb.set(simbolo[0])
            menuOpciones = OptionMenu(frame4,simb,*simbolo)
            menuOpciones.grid(row=i,column=columCount)
            columCount+=1

            cuadrito = Entry(frame4,width=5,relief=RAISED)
            funcEspacios[i+1].append(cuadrito)       #necesito control de cuadritos
            cuadrito.grid(row=i,column=columCount)
            columCount+=1


            funcEspacios[i+1].append(simb)

        lin = Label(frame4,text="")
        lin.grid(row=9,sticky=W)

        self.button2 = Button(frame4,text="Aceptar", relief = RAISED,command = lambda:self.printear(self.opcion,variables,restricciones,funcEspacios,self.button2))
        self.button2.grid(row=10,sticky=W)


    # def matriciar(self,master,opcion,variables,restricciones,funcEspacios,button2):
    #     button2.destroy()
    #     simbolos = []
    #     for s in range(1,len(funcEspacios)):            #simbolos de restricciones
    #         simbolos.append(funcEspacios[s][-1])
    #
    #     frame3 = Frame(master)
    #     frame3.pack(side=TOP)
    #     filas = restricciones
    #     columnas = variables
    #     matriz = []
    #     for fv in range(1,variables+1):         #fila de arriba
    #         x = "X"+str(fv)+" "
    #         xs = Label(frame3,text=x,width=5)
    #         xs.grid(row=0,column=fv)
    #     d = Label(frame3,text="D",width=5)
    #     d.grid(row=0,column=variables+1)
    #
    #     for f in range(1,filas+2):
    #         matriz.append([])
    #         if (f==1):                  #funcion MaxU
    #             z = Label(frame3,text="Z ",width=5)
    #             z.grid(row=f,column=0)
    #             for c1 in range(columnas):
    #                 matriz[f-1].append(Entry(frame3,width=5,relief=RAISED))
    #                 #print(funcEspacios[0][c1].get())
    #                 matriz[f-1][c1].insert(0,funcEspacios[0][c1].get())
    #                 matriz[f-1][c1].config(state="readonly")
    #                 matriz[f-1][c1].grid(row=f,column=c1+1)
    #
    #             matriz[f-1].append(Entry(frame3,width=5,relief=RAISED))
    #             matriz[f-1][columnas].insert(0,0)
    #             matriz[f-1][columnas].config(state="readonly")
    #             matriz[f-1][columnas].grid(row=f,column=columnas+1)
    #
    #         else:               #resto de matriz
    #             x = "X"+str(variables+f)+" "
    #             xl = Label(frame3,text=x,width=5)
    #             xl.grid(row=f,column=0)
    #             for c in range(columnas+1):
    #                 matriz[f-1].append(Entry(frame3,width=5,relief=RAISED))
    #                 matriz[f-1][c].grid(row=f,column=c+1)
    #
    #
    #
    #     for x in range(1,len(matriz)):
    #         for y in range(0,len(matriz[x])):
    #             matriz[x][y].insert(0,funcEspacios[x][y].get())
    #             matriz[x][y].config(state="readonly")
    #
    #     self.button5 = Button(frame3,text="Aceptar", relief = RAISED,command = lambda:self.printear(opcion,variables,restricciones,matriz,simbolos,funcEspacios))
    #     self.button5.grid(row=10)


    def printear(self,opcion,variables,restricciones,funcEspacios,button2):

        button2.destroy()
        simbolos = []
        for s in range(1,len(funcEspacios)):            #simbolos de restricciones
            simbolos.append(funcEspacios[s][-1].get())

        resultado = []
        resultado.append(opcion.get())        #pega la opcion max o min
        resultado.append(str(variables)+","+str(restricciones)) #pega num variablesy restricciones

        linea = []
        for x in funcEspacios[0]:
            linea.append(x.get())
        resultado.append(linea)         #pega la funcion max o min

        for x in range(1,restricciones+1):
            linea = []
            for y in range(0,len(funcEspacios[x])-1):
                linea.append(funcEspacios[x][y].get())
            linea.append(simbolos[x-1])
            resultado.append(linea)     #pega lineas de la matriz


        for lis in range(2,len(resultado)):
            for lisItem in resultado[lis]:
                print(lisItem)
                listaCambiada.append(lisItem)



        modificar(variables,restricciones,opcion)
        print(resultado)


root = Tk()
root.geometry("600x400")
root.resizable(True, False)
matriz = matrizDatos(root)
root.mainloop()
