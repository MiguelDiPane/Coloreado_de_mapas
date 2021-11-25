import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter.constants import N,S,W,E
import numpy as np
import turtle
from random import randint, seed


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        #----------------------------#
        # Configuraciones generales  #
        #----------------------------#
        self.title("TDA: Grafo")
        self.fuente = font.Font(weight='normal')

        #----------------------------#
        #       Menu de opciones     #
        #----------------------------#

        self.barraMenu=tk.Menu(self)
        self.menuArchivo=tk.Menu(self.barraMenu, tearoff=0)
        self.menuFunciones=tk.Menu(self.barraMenu, tearoff=0)
        
        self.barraMenu.add_cascade(label="Inicio", menu=self.menuArchivo)
        self.barraMenu.add_cascade(label="Herramientas", menu=self.menuFunciones)

        self.config(menu=self.barraMenu)

        #-----------------------------------------------------#
        #   Frame de la matriz y características del grafo    #
        #-----------------------------------------------------#

        self.contenedor = Contenedor(self)
        self.contenedor.grid(padx=5, pady=5, row=0, column=0, sticky=(N))

        #-------------------------#
        #   Frame para dibujo     #
        #-------------------------#
        
        self.lienzo = Lienzo(self,600,600)
        self.lienzo.grid(padx=5, pady=5, row=0, column=1, sticky=(N,W,E,S))

    def setControlador(self,ctrl):
        '''Vincula los metodos del controlador con la vista'''

        #Menú inicio
        self.menuArchivo.add_command(label="Nuevo grafo", command=ctrl.nuevo)
        self.menuArchivo.add_separator()
        self.menuArchivo.add_command(label='Salir', command=self.destroy)

        #Menú herramientas
        self.menuFunciones.add_command(label="Dibujar y colorear grafo", command=ctrl.dibujar)
        self.menuFunciones.add_command(label="Encontrar caminos", command=ctrl.caminos)
        self.menuFunciones.add_command(label="Explorar nodos", command=ctrl.adyacentes)

        print("Controlador seteado")
    
    def mostrar_mensaje(self,resultado):
        '''Muestra el mensaje de éxito o falla al buscar la solución'''
        if resultado == "exito":
            messagebox.showinfo("Solución encontrada!","La cantidad de colores ingresada permite resolver el problema.")
        elif resultado == "fracaso":
            messagebox.showerror("La solución no existe","La cantidad de colores ingresada no permite resolver el problema.")

    def abrir(self):
        print('Abrir')
    
      
class Contenedor(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padx=10, pady=10, **kwargs)
        #Valores iniciales al iniciar el programa
        self.matriz = MatrizAdyacencia(self)
        self.informacion = InfoGrafo(self)
        self.matriz.grid(padx=5, pady=5, row=0, column=0)
        self.informacion.grid(padx=5, pady=5, row=1, column=0,sticky=(E,W))

class MatrizAdyacencia(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Matriz de adyacencia / pesos", padx=10, pady=10, **kwargs)
        #Valores iniciales al iniciar el programa
        self.cantNodos = 6
        self.tipo = "Grafo"
        self.representacion = "Secuencial"
        self.inicializar_casillas()

    def inicializar_casillas(self):
        #Borro la grilla actual
        for widget in self.winfo_children():
            widget.destroy()    

        self.casillas = np.full((self.cantNodos,self.cantNodos),None)

        for r in range(self.cantNodos):
            etiqueta_nodo = ttk.Label(self, text=str(r), padding=(5,5))
            etiqueta_nodo.grid(padx=5, pady=5, row=0, column=r+1) #en fila 0
            for c in range(self.cantNodos):   
                etiqueta_nodo = ttk.Label(self, text=str(r), padding=(5,5))
                etiqueta_nodo.grid(padx=5, pady=5, row=r+1, column=0) #en columna 0
                casilla = tk.Entry(self,width=5)
                if self.tipo == 'Grafo' and self.representacion == 'Secuencial':
                    if c > r:
                        texto = tk.StringVar()
                        texto.set('0')
                        casilla = tk.Entry(self,width=5, state='disabled',textvariable=texto)
                        
                casilla.grid(padx=5, pady=5, row=r+1, column=c+1)
                casilla.insert(0, '0')
                self.casillas[r][c] = casilla
    
    def obtenerMatriz(self):
        matriz = np.full((self.cantNodos,self.cantNodos),0)
        for i in range(self.cantNodos):
            for j in range(self.cantNodos):
                matriz[i][j] = self.casillas[i][j].get()
        return matriz

class InfoGrafo(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Características", padx=10, pady=10, **kwargs)
        
        #Valores iniciales al iniciar el programa
        self.cant_nodos = 6
        self.tipo = "Grafo"
        self.representacion = "Secuencial"
        self.mostrar_etiquetas()
 
    def cambiar_caracteristicas(self,cant_nodos,tipo,representacion):
        self.cant_nodos = cant_nodos
        self.tipo = tipo
        self.representacion = representacion
        self.mostrar_etiquetas()
    
    def mostrar_etiquetas(self):
        text_cant_nodos = "Cantidad de nodos: {}".format(self.cant_nodos)
        text_tipo = "Tipo: {}".format(self.tipo)
        text_representacion = "Representación: {}".format(self.representacion)

        self.txt_cantN = tk.StringVar()
        self.txt_cantN.set(text_cant_nodos)
        self.txt_tipo = tk.StringVar()
        self.txt_tipo.set(text_tipo)
        self.txt_rep = tk.StringVar()
        self.txt_rep.set(text_representacion)
        
        lbl_nodos = ttk.Label(self, textvariable=self.txt_cantN)
        lbl_nodos.grid(padx=5, pady=5, row=0, column=0,sticky=(W))
        lbl_tipo = ttk.Label(self, textvariable=self.txt_tipo)
        lbl_tipo.grid(padx=5, pady=5, row=1, column=0,sticky=(W))
        lbl_rep = ttk.Label(self, textvariable=self.txt_rep)
        lbl_rep.grid(padx=5, pady=5, row=2, column=0,sticky=(W))

        self.texto_camino = tk.StringVar()
        self.texto_camino.set("")
        self.lbl_camino = tk.Label(self, textvariable=self.texto_camino)

class Lienzo(tk.Canvas):

    def __init__(self, master,alto,ancho, **kwargs):
        super().__init__(master,height=alto,width=ancho)

        #---------------------------#
        # Configuraciones del lápiz #
        #---------------------------#
        self.configure(background='black')

        self.dibujador = turtle.RawTurtle(self) #Le paso el canvas al dibujador
        self.dibujador.hideturtle()
        self.dibujador.speed(0)
        self.dibujador.color('black')  
    
    def dibujarGrafo(self,matriz,colores):
        self.limpiarLienzo()

        cantNodos = len(matriz)

        #seed(111231231)
        
        #Grafica de los nodos
        posiciones = []
     
        #Extraigo colores sin repetidos, para generar los códigos hexa
        mis_colores = []
        for color in colores:
            if color not in mis_colores:
                mis_colores.append(color)
        
        #Genero cadenas entre 000000 y FFFFFF aleatorias segun cant de colores que vienen en el parámetro de entrada
        mis_colores_hexa = []
        for color in mis_colores:
            #Genero 6 numeros aleatorios entre 0 y 15 para generar el caracter
            color_string = "#"
            for i in range(6):
                letra_ascii = randint(65,70) #De A a F
                numero_ascii = randint(48,57) #De 0 a 9
                elegir = randint(0,1)
                if elegir == 0:
                    cod_ascii = letra_ascii #Va a usar una letra
                else:
                    cod_ascii = numero_ascii #Va a usar un numero
                #Convierto el codigo ascii a caracter y lo agrego al string
                caracter = chr(cod_ascii)
                color_string += caracter
            mis_colores_hexa.append(color_string)

        radio = 10

        #Dibujo los nodos en un círculo
        alfa = 2*np.pi / cantNodos #Angulo de separacion entre nodos, en radianes
        radio_dibujo = 200

        for i in range(cantNodos):
            #Posicion usando la ec  sen(alfa) = x / radio y cos(alfa) = y / radio
            x = radio_dibujo * np.sin(alfa * i)
            y = radio_dibujo * np.cos(alfa * i)

            nueva_pos = (x,y)
            posiciones.append(nueva_pos)

            self.dibujador.penup()
            self.dibujador.goto(nueva_pos)
            self.dibujador.pendown()
            
            numero_color = colores[i] #Obtengo el numero de color del nodo
            color_nodo = mis_colores_hexa[numero_color]
            
            self.dibujador.fillcolor(color_nodo)
            self.dibujador.begin_fill()
            self.dibujador.circle(radio,360)
            self.dibujador.end_fill()
            self.dibujador.penup()
            self.dibujador.setposition(nueva_pos[0]+30,nueva_pos[1]+15)
            self.dibujador.write(str(i),font=('Arial', 10, 'bold'))
        
        #Grafica de las relaciones
        for i in range(cantNodos):
            for j in range(cantNodos):
                if matriz[i][j] > 0:
                    if i != j:
                        #Dibujo la linea desde i hasta j
                        self.dibujador.penup()
                        pos = posiciones[i]
                        self.dibujador.goto(pos[0],pos[1]+radio)
                        self.dibujador.pendown()
                        pos = posiciones[j]
                        self.dibujador.goto(pos[0],pos[1]+radio)
                    else:
                        #Dibujo bucle   
                        self.dibujador.penup()
                        pos = posiciones[i]
                        self.dibujador.goto(pos[0],pos[1]+radio)
                        self.dibujador.pendown()
                        self.dibujador.circle(radio,360)
                    
    def limpiarLienzo(self):
        self.dibujador.clear()

class ventanaNuevoGrafo(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Nuevo grafo")

        self.tipo = parent.contenedor.matriz.tipo
        self.representacion = parent.contenedor.matriz.representacion
        self.cant_nodos = parent.contenedor.matriz.cantNodos

        lbl_tipo = tk.Label(self, text="Tipo")
        lbl_tipo.grid(padx=5, pady=5, row=0, column=0)

        self.combo_tipo = ttk.Combobox(self, width=10)
        self.combo_tipo["values"] = ["Grafo", "Digrafo"]
        self.combo_tipo.current(0)
        self.combo_tipo.grid(padx=5, pady=5, row=0, column=1,sticky=(E,W))

        lbl_tipo = tk.Label(self, text="Representación")
        lbl_tipo.grid(padx=5, pady=5, row=1, column=0)

        self.combo_representacion = ttk.Combobox(self, width=10)
        self.combo_representacion["values"] = ["Secuencial", "Enlazada"]
        self.combo_representacion.current(0)
        self.combo_representacion.grid(padx=5, pady=5, row=1, column=1,sticky=(E,W))

        lbl_cantNodos = tk.Label(self, text="N° de nodos")
        lbl_cantNodos.grid(padx=5, pady=5, row=2, column=0)

        self.entry_cantNodos = ttk.Entry(self)
        self.entry_cantNodos.grid(padx=5, pady=5, row=2, column=1, sticky=(E,W))
       
        self.btn_cancelar = tk.Button(self, text="Cancelar", command=self.destroy)
        self.btn_cancelar.grid(padx=5, pady=5, row=3, column=0,sticky=(W))
        self.btn_cancelar.focus_set()

        self.btn_aceptar = tk.Button(self, text="Aceptar", command=self.aceptar)
        self.btn_aceptar.grid(padx=5, pady=5, row=3, column=1,sticky=(E))
 
    def aceptar(self):
        #Valida la selección de los datos antes de destruir la ventana y retornar los datos en mostrar()
        if self.entry_cantNodos.get() == '':
            print("Debe ingresar la cantidad de nodos")
        else:
            self.tipo = self.combo_tipo.get()
            self.representacion = self.combo_representacion.get()
            self.cant_nodos = self.entry_cantNodos.get()
            self.destroy()
    
    def mostrar(self):
        #Retorna
        self.grab_set()
        self.wait_window()

        #Retorna los datos para crear el nuevo grafo
        return self.tipo,self.representacion,self.cant_nodos

class ventanaInfoNodo(tk.Toplevel):
    def __init__(self,parent,controlador):
        super().__init__(parent)
        self.title("Explorador de nodos")

        lbl_titulo = tk.Label(self, text="Ingrese un nodo para ver su información")
        lbl_titulo.grid(padx=5, pady=5, row=0, column=0)

        lbl_nodo = tk.Label(self, text="Nodo")
        lbl_nodo.grid(padx=5, pady=5, row=1, column=0)

        self.entry_nodo = ttk.Entry(self)
        self.entry_nodo.grid(padx=5, pady=5, row=1, column=1, sticky=(E,W))

        lbl_nodo = tk.Label(self, text="Adyacentes")
        lbl_nodo.grid(padx=5, pady=5, row=2, column=0)

        self.texto_ady = tk.StringVar()
        self.texto_ady.set("")
        self.lbl_adyacentes = tk.Label(self, textvariable=self.texto_ady)
        self.lbl_adyacentes.grid(padx=5, pady=5, row=2, column=1, sticky=(E,W))

        lbl_nodo = tk.Label(self, text="Grado")
        lbl_nodo.grid(padx=5, pady=5, row=3, column=0)
        self.texto_grado = tk.StringVar()
        self.texto_grado.set("")
        self.lbl_adyacentes = tk.Label(self, textvariable=self.texto_grado)
        self.lbl_adyacentes.grid(padx=5, pady=5, row=3, column=1, sticky=(E,W))

        self.btn_cancelar = tk.Button(self, text="Cerrar", command=self.destroy)
        self.btn_cancelar.grid(padx=5, pady=5, row=4, column=0,sticky=(W))
        self.btn_cancelar.focus_set()

        self.btn_aceptar = tk.Button(self, text="Mostrar información", command=controlador.mostrar_info_nodo)
        self.btn_aceptar.grid(padx=5, pady=5, row=4, column=1,sticky=(E))
 
    def mostrar(self):
        #Retorna
        self.grab_set()
        self.wait_window()

class ventanaCaminos(tk.Toplevel):
    def __init__(self,parent,controlador):
        super().__init__(parent)
        self.title("Camino entre nodos")

        lbl_titulo = tk.Label(self, text="Ingrese un nodo origen y un nodo destino")
        lbl_titulo.grid(padx=5, pady=5, row=0, column=0)

        lbl_nodo_origen = tk.Label(self, text="Nodo origen")
        lbl_nodo_origen.grid(padx=5, pady=5, row=1, column=0)

        self.entry_nodo_origen = ttk.Entry(self)
        self.entry_nodo_origen.grid(padx=5, pady=5, row=1, column=1, sticky=(E,W))

        lbl_nodo_destino = tk.Label(self, text="Nodo destino")
        lbl_nodo_destino.grid(padx=5, pady=5, row=2, column=0)

        self.entry_nodo_destino = ttk.Entry(self)
        self.entry_nodo_destino.grid(padx=5, pady=5, row=2, column=1, sticky=(E,W))


        lbl_cam = tk.Label(self, text="Camino")
        lbl_cam.grid(padx=5, pady=5, row=3, column=0)

        self.texto_camino = tk.StringVar()
        self.texto_camino.set("")
        self.lbl_camino = tk.Label(self, textvariable=self.texto_camino)
        self.lbl_camino.grid(padx=5, pady=5, row=3, column=1, sticky=(E,W))

        lbl_cam_min = tk.Label(self, text="Camino mínimo")
        lbl_cam_min.grid(padx=5, pady=5, row=4, column=0)

        self.texto_camino_min = tk.StringVar()
        self.texto_camino_min.set("")
        self.lbl_camino_min = tk.Label(self, textvariable=self.texto_camino_min)
        self.lbl_camino_min.grid(padx=5, pady=5, row=4, column=1, sticky=(E,W))

        self.btn_cancelar = tk.Button(self, text="Cerrar", command=self.destroy)
        self.btn_cancelar.grid(padx=5, pady=5, row=5, column=0,sticky=(W))
        self.btn_cancelar.focus_set()

        self.btn_aceptar = tk.Button(self, text="Mostrar caminos", command=controlador.mostrar_caminos)
        self.btn_aceptar.grid(padx=5, pady=5, row=5, column=1,sticky=(E))
 
    def mostrar(self):
        #Retorna
        self.grab_set()
        self.wait_window()      

class ventanaCantidadColores(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Colores")
        self.m = 3 #Cantidad de colores

        lbl_nodo_origen = tk.Label(self, text="Ingrese la cantidad de colores")
        lbl_nodo_origen.grid(padx=5, pady=5, row=0, column=0)

        lbl_cant = tk.Label(self, text="Cantidad")
        lbl_cant.grid(padx=5, pady=5, row=1, column=0)

        self.cantColores = tk.StringVar()
        self.cantColores.set("3")
        self.entry_cantColores = ttk.Entry(self, textvariable=self.cantColores)
        self.entry_cantColores.grid(padx=5, pady=5, row=1, column=1, sticky=(E,W))
       
        self.btn_cancelar = tk.Button(self, text="Cancelar", command=self.destroy)
        self.btn_cancelar.grid(padx=5, pady=5, row=2, column=0,sticky=(W))
        self.btn_cancelar.focus_set()

        self.btn_aceptar = tk.Button(self, text="Aceptar", command=self.aceptar)
        self.btn_aceptar.grid(padx=5, pady=5, row=2, column=1,sticky=(E))
 
    def aceptar(self):
        #Valida la selección de los datos antes de destruir la ventana y retornar los datos en mostrar()
        if self.entry_cantColores.get() == '':
            print("Debe ingresar la cantidad de nodos")
        else:
            self.m = int(self.entry_cantColores.get())
            self.destroy()
    
    def mostrar(self):
        #Retorna
        self.grab_set()
        self.wait_window()

        #Retorna la cantidad de colores para pintar el grafo
        return self.m
