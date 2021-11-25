from grafos.claseDigrafoEnlazado import DigrafoEnlazado
from grafos.claseDigrafoSecuencial import DigrafoSecuencial
from grafos.claseGrafoEnlazada import GrafoEnlazado
from grafos.claseGrafoSecuencial import GrafoSecuencial

class Relacion:
    def __init__(self,nodo_i,nodo_j,peso):
        self.i = nodo_i
        self.j = nodo_j
        self.peso = peso

class Modelo:
    
    def __init__(self):
        self.grafo = None
        self.cant_nodos = 0
        self.relaciones = None

    def crear_grafo(self,matriz,tipo,representacion):
        self.cant_nodos = len(matriz)
        self.relaciones = self.construir_relaciones(matriz)

        if tipo == "Grafo":
            if representacion == "Enlazada":
                self.grafo = GrafoEnlazado(self.cant_nodos)
            elif representacion == "Secuencial":

                self.grafo = GrafoSecuencial(self.cant_nodos)
        elif tipo == "Digrafo":
            if representacion == "Enlazada":
                self.grafo = DigrafoEnlazado(self.cant_nodos)
            elif representacion == "Secuencial":
                self.grafo = DigrafoSecuencial(self.cant_nodos)
        
        for i in range(self.cant_nodos):
            self.grafo.cargar_nodo(i)
        for rel in self.relaciones:
            self.grafo.relacionar_nodos(rel.i,rel.j,rel.peso)

    def construir_relaciones(self,matriz):
        relaciones = []
        for i in range(len(matriz)):
            for j in range(len(matriz)):
                peso = matriz[i][j]
                nueva_relacion = Relacion(i,j,peso)
                relaciones.append(nueva_relacion)
        return relaciones
  
    def pedir_adyacentes(self,nodo):
        return self.grafo.adyacentes(nodo)
    
    def pedir_grado(self,nodo):
        return self.grafo.grado(nodo)
    
    def pedir_camino(self,nodo_origen,nodo_destino):
        return self.grafo.camino(nodo_origen,nodo_destino)

    def pedir_camino_min(self,nodo_origen,nodo_destino):
        return self.grafo.camino_minimo(nodo_origen,nodo_destino)
    
    def pedir_conexidad(self):
        return self.grafo.conexo()

    def pedir_aciclico(self):
        return self.grafo.aciclico()

    #--------------------------------------#
    #       MÉTODOS PARA EL COLOREADO      #
    #--------------------------------------#

    # método para chequear que el color actual asignado sea seguro para el vértice v
    def es_adecuado(self, nodo, lista_colores, color):
        #A partir del nodo ingresado, controla todos los demás nodos para ver si hay relación
        #Y para ver si el color de v es igual al de algún otro nodo i
        adecuado = True
        adyacentes_a_nodo = self.grafo.adyacentes(nodo)
        for i in adyacentes_a_nodo:
            if lista_colores[i] == color:
                adecuado = False
        return adecuado
    
    #Metodo recursivo para resolver el problema del coloreado de n vértices
    def pintado_recursivo(self, cant_colores, lista_colores, nodo):
        if nodo == self.cant_nodos:
            return True
        #Si termina el for sin encontrar color adecuado, retorna None
        for color in range(1, cant_colores+1):
            adecuado = self.es_adecuado(nodo, lista_colores, color)
            if adecuado:
                lista_colores[nodo] = color
                if self.pintado_recursivo(cant_colores, lista_colores, nodo+1) == True:
                    return True
                else:
                    lista_colores[nodo] = 0
                    return False
        return None
 
    def colorear_grafo(self, cant_colores):
        solucion = False
        lista_colores = [0] * self.cant_nodos
        if self.pintado_recursivo(cant_colores, lista_colores, 0) == False:
            print("La solución no existe")
        else:
            #Resto 1 a todos los colores para usarlos como índices
            for i in range(self.cant_nodos):
                lista_colores[i] -= 1
            # Retorno la lista con los colores para cada nodo, ordenados por su índice
            print("La solución existe")
            solucion = lista_colores
        return solucion