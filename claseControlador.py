from claseVista import ventanaCaminos, ventanaCantidadColores, ventanaNuevoGrafo, ventanaInfoNodo

class Controlador:
    def __init__(self,vista,modelo):
        self.ventana = vista
        self.modelo = modelo

        self.ventana_adyacentes = None
        self.ventana_caminos = None

    def iniciar(self):
        self.ventana.mainloop()

    def crear_grafo(self):
        matriz = self.ventana.contenedor.matriz.obtenerMatriz()
        tipo = self.ventana.contenedor.matriz.tipo
        representacion = self.ventana.contenedor.matriz.representacion
        self.modelo.crear_grafo(matriz,tipo,representacion)
    
    #----------------------------------------------#
    #   MÉTODOS QUE CONTROLAN EL MENÚ DE OPCIONES  #
    #----------------------------------------------#

    def nuevo(self):
        tipo, representacion, cant_nodos = ventanaNuevoGrafo(self.ventana).mostrar()

        #Iniciar nuevo grafo
        self.ventana.contenedor.matriz.cantNodos = int(cant_nodos)
        self.ventana.contenedor.matriz.tipo = tipo
        self.ventana.contenedor.matriz.representacion = representacion
        self.ventana.contenedor.matriz.inicializar_casillas()
        self.ventana.lienzo.limpiarLienzo()
        self.ventana.contenedor.informacion.cambiar_caracteristicas( cant_nodos,tipo,representacion)

    def adyacentes(self):
        self.ventana_info_nodo = ventanaInfoNodo(self.ventana,self)
        self.ventana_info_nodo.mostrar()
    
    def caminos(self):
        self.ventana_caminos = ventanaCaminos(self.ventana,self)
        self.ventana_caminos.mostrar()
        
    #-------------------------------------------#
    #   MÉTODO PARA MOSTRAR Y PINTAR EL GRAFO   #
    #-------------------------------------------#

    def dibujar(self):
        matriz = self.ventana.contenedor.matriz.obtenerMatriz()
        self.crear_grafo()
        
        #Pedir cantidad de colores
        cant_colores = ventanaCantidadColores(self.ventana).mostrar()

        #Llamada al método de coloreado
        colores = self.modelo.colorear_grafo(cant_colores)
        if colores != False:
            self.ventana.mostrar_mensaje("exito")
        else:
            #Pongo todos en un solo color
            self.ventana.mostrar_mensaje("fracaso")
            colores = [0] * len(matriz)

        self.ventana.lienzo.dibujarGrafo(matriz,colores)
    
    #------------------------------#
    #   OPERACIONES CON EL GRAFO   #
    #------------------------------#

    def mostrar_info_nodo(self):

        #Valida la selección de los datos antes de destruir la ventana y retornar los datos en mostrar()
        if self.ventana_info_nodo.entry_nodo.get() == '':
            texto_ady = "Debe ingresar un nodo"
            texto_grado = "Debe ingresar un nodo"
        else:
            self.crear_grafo()
            nodo = int(self.ventana_info_nodo.entry_nodo.get())
            adyacentes = self.modelo.pedir_adyacentes(nodo)
            grado = self.modelo.pedir_grado(nodo)
            texto_ady = "{}".format(adyacentes)
            texto_grado = "{}".format(grado)

        self.ventana_info_nodo.texto_ady.set(texto_ady)
        self.ventana_info_nodo.texto_grado.set(texto_grado)
    
    def mostrar_caminos(self):
        if self.ventana_caminos.entry_nodo_destino.get() != '' and self.ventana_caminos.entry_nodo_origen.get() != '':
            self.crear_grafo()
            nodo_origen = int(self.ventana_caminos.entry_nodo_origen.get())
            nodo_destino = int(self.ventana_caminos.entry_nodo_destino.get())
            camino = self.modelo.pedir_camino(nodo_origen,nodo_destino)
            camino_min = self.modelo.pedir_camino_min(nodo_origen,nodo_destino)
            texto_camino = "{}".format(camino)
            texto_camino_min = "{}".format(camino_min)
        
            self.ventana_caminos.texto_camino.set(texto_camino)
            self.ventana_caminos.texto_camino_min.set(texto_camino_min)

