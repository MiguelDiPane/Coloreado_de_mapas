import numpy as np
from .claseColas import ColaEncadenada
from rich.table import Table
from rich import print

class Nodo:
    def __init__(self,dato=None):
        self.dato = dato

class Registro:
    def __init__(self,nodo,conocido,distancia,camino):
        self.nodo = nodo
        self.conocido = conocido
        self.distancia = distancia
        self.camino = camino

class Datos:
    def __init__(self,recorrido=None, nodos_visitados=None, predecesores=None, hay_ciclo=None):
        self.recorrido = recorrido
        self.nodos_visitados = nodos_visitados
        self.predecesores = predecesores
        self.hay_ciclo = hay_ciclo
   
class GrafoSecuencial:
    '''Grafo con Representación Secuencial, ponderado o no'''

    def __init__(self,cant_nodos,ponderado=False):
        self.__cantNodos = cant_nodos
        self.__ponderado = ponderado

        #Trabajar con representación unidimensional, en digrafo usar matriz nxn
        self.__cant_componentes = int(self.__cantNodos*(self.__cantNodos+1)/2) #n(n+1)/2
        
        #Si es ponderado se carga con datos, sino con 0 o 1 (adyacencia)
        self.__arreglo = np.full(self.__cant_componentes,0)
        self.__nodos = np.full(self.__cantNodos,None)

    def cargar_nodo(self,nodo,dato=None):
        '''Carga el nodo ingresado con un dato'''
        try:
            self.__validar_indices(nodo)
            nuevo_nodo = Nodo(dato)
            self.__nodos[nodo] = nuevo_nodo
        except ValueError as error:
            print(error)

    def relacionar_nodos(self,i,j,peso=1):
        '''Enlaza dos nodos a traves de la matriz de adyacencia o de pesos'''
        try:
            self.__validar_indices(i,j)
            pos = self.__obtener_posicion(i,j)
            self.__arreglo[pos] = peso
        except ValueError as error:
            print(error)
 
    def adyacentes(self,i):
        '''Determina los nodos adyacentes del nodo ingresado'''
        nodos_adyacentes = []
        try:
            self.__validar_indices(i)
            for j in range(self.__cantNodos):
                pos = self.__obtener_posicion(i,j)
                if self.__arreglo[pos] > 0: #si tiene peso puede ser mayor a 1
                    nodos_adyacentes.append(j)
        except ValueError as error:
            print(error)
        return nodos_adyacentes

    def grado(self,nodo):
        '''Retorna el grado de un nodo, número de aristas en las que participa'''
        adyacentes = self.adyacentes(nodo)
        return len(adyacentes)
 
    def camino(self,nodo_inicial,nodo_destino,mostrar_camino=False):
        """Aplica búsqueda en profundidad para encontrar un camino (no necesariamente el mínimo)"""
        camino = []
        try:
            self.__validar_indices(nodo_inicial,nodo_destino)
            datos = self.busqueda_en_profundidad_REP(nodo_inicial)
            predecesores = datos.predecesores
            camino = self.__reconstruir_camino(nodo_destino,predecesores)
            if mostrar_camino:
                print("Camino desde {} a {}: {}".format(nodo_inicial,nodo_destino,camino))
        except ValueError as error:
            print(error)
        return camino
  
    def camino_minimo(self,nodo_inicial,nodo_destino,mostrar_mensaje = False):
        '''Si es ponderado busca el camino con el menor peso total, aplica Dijkstra, sino REA, camino con menor numero de aristas'''
        camino = []
        try: 
            self.__validar_indices(nodo_inicial,nodo_destino)
            if self.__ponderado:
                predecesores = self.algoritmo_Dijkstra(nodo_inicial)              
            else:
                datos = self.busqueda_en_amplitud_REA(nodo_inicial)
                predecesores = datos.predecesores
            camino = self.__reconstruir_camino(nodo_destino,predecesores)
                
            if mostrar_mensaje:
                print("Camino mínimo entre {0} y {1}: {2}".format(nodo_inicial,nodo_destino,camino))
        except ValueError as error:
            print(error)
        return camino

    def conexo(self):
        '''Aplica la búsqueda en aplitud para analizar la conexidad'''
        #Un grafo G es conexo, si al menos existe un camino entre cada par de nodos del grafo
        i = 0
        es_conexo = True
        while i < self.__cantNodos and es_conexo:
            datos = self.busqueda_en_amplitud_REA(i)
            if False in datos.nodos_visitados:
                es_conexo = False
            i+=1
        return es_conexo

    def aciclico(self):
        '''Evalua si el grafo tiene ciclos o no, aplica búsqueda en amplitud para cada nodo'''
        #Ciclo: camino simple (todos los nodos son distintos, salvo v0 y vn) cerrado de longitud 3 o mas
        es_aciclico = True   
        i = 0
        while i < self.__cantNodos and es_aciclico:
            datos = self.busqueda_en_amplitud_REA(i)
            if datos.hay_ciclo:
                es_aciclico = False
            i+=1
        return es_aciclico

    def obtener_arbol_de_recubrimiento_minimo(self,nodo_origen):
        '''Aplica algoritmo de Prim'''
        #Encuentra un arbol de recubrimiento mínimo (mínimo peso total) en un grafo conexo, no dirigido y con aristas ponderadas
        if self.__ponderado and self.conexo():
            T = self.__crear_tabla_T()

            #Vertice inicial
            T[nodo_origen].distancia = 0

            for _ in range(self.__cantNodos):
                v = self.__obtener_vertice_dist_mas_corta_desconocido(T)
                T[v].conocido = True
                adyacentes_a_v = self.adyacentes(v)
                for w in adyacentes_a_v:
                    if T[w].conocido == False:
                        pos = self.__obtener_posicion(v,w)
                        if self.__arreglo[pos] < T[w].distancia:
                            T[w].distancia = self.__arreglo[pos]
                            T[w].camino = v #agrego v al camino 
            self.__mostrar_tabla_T(T)
        else:
            print('El grafo debe ser conexo ponderado para determinar su árbol de recubrimiento mínimo')

    #------------------------------------#
    # ALGORITMOS DE BÚSQUEDA O RECORRIDO #
    #------------------------------------#

    def busqueda_en_amplitud_REA(self,nodo_origen):
        '''Algoritmo: Procesa todos los elementos del grafo en anchura, dado un nodo buscar
        todos los adyacentes, luego de cada uno sus adyacantes hasta completar la búsqueda'''

        cola =  ColaEncadenada()
        #todos los nodos están NO marcados  
        nodos_visitados = np.full(self.__cantNodos,False)
        #Almacena que nodo precede al nodo correspondiente a la posición i del arreglo
        predecesores = np.full(self.__cantNodos,None)
        #Recorrido en anchura realizado
        recorrido = []

        hay_ciclo = False

        nodos_visitados[nodo_origen] = True #marcar el origen

        cola.insertar(nodo_origen)
        while not cola.vacia():
            nodo_v = cola.suprimir()
            recorrido.append(nodo_v)
            nodos_u = self.adyacentes(nodo_v)
        
            for u in nodos_u:
                adyacentes_a_u = self.adyacentes(u)
                #Para buscar un ciclo, veo si v esta en los adyacentes de u, con uno me basta para determinar 
                #si es o no acíclico
                if nodo_v in adyacentes_a_u and not hay_ciclo:
                    hay_ciclo = True

                if nodos_visitados[u] == False:
                    nodos_visitados[u] = True #marcar u
                    predecesores[u] = nodo_v #Guardo el predecesor
                    cola.insertar(u)
        
        mis_datos = Datos(recorrido, nodos_visitados, predecesores, hay_ciclo)
        return mis_datos
    
    def busqueda_en_profundidad_REP(self,s,start=True,**kwargs):
        if start:
            nodos_visitados = np.full(self.__cantNodos,False)
            recorrido = []
            predecesores = np.full(self.__cantNodos,None)
        else:
            nodos_visitados = kwargs['nodos_visitados']
            recorrido = kwargs['recorrido']
            predecesores = kwargs['predecesores']

        nodos_visitados[s] = True
        recorrido.append(s)
        adyacentes_a_s = self.adyacentes(s)
        for nodo in adyacentes_a_s:
            if not nodos_visitados[nodo]:
                predecesores[nodo] = s
                self.busqueda_en_profundidad_REP(nodo,False,
                                        nodos_visitados = nodos_visitados,
                                        recorrido = recorrido,
                                        predecesores = predecesores)
        mis_datos = Datos(recorrido,nodos_visitados,predecesores)
        return mis_datos

    def algoritmo_Dijkstra(self,nodo_origen):
        '''Algoritmo: determina el camino más corto desde un nodo origen 
        al resto de nodos en un grafo PONDERADO'''
        T = self.__crear_tabla_T()

        #Vertice inicial
        T[nodo_origen].distancia = 0

        for _ in range(self.__cantNodos):
            v = self.__obtener_vertice_dist_mas_corta_desconocido(T)
            T[v].conocido = True
            adyacentes_a_v = self.adyacentes(v)
            for w in adyacentes_a_v:
                if T[w].conocido == False:
                    pos = self.__obtener_posicion(v,w)
                    if (T[v].distancia + self.__arreglo[pos]) < T[w].distancia:
                        #Reducir T[w].distancia a T[v].distancia + w(v,w)
                        T[w].distancia = T[v].distancia + self.__arreglo[pos]
                        T[w].camino = v #agrego v al camino 
        self.__mostrar_tabla_T(T)
        caminos = self.__obtener_caminos_de_tabla_T(T)
        return caminos

    #------------------------#
    #   METODOS AUXILIARES   #
    #------------------------#
 
    def __validar_indices(self,i,j=0):
        #Lanza una excepción en caso de índices no validos
        if i < 0 or j < 0 or i >= self.__cantNodos or j >= self.__cantNodos:
            raise ValueError('Indices no válidos')
   
    def __obtener_posicion(self,i,j):
        i+= 1
        j+= 1
        #Obtiene la posición del arreglo de enlaces trabajando con matriz triangular inferior
        if i <= j:
            aux = j 
            j = i
            i = aux
        pos = int(i *(i-1)/2 + j)
        return pos - 1 #Para que sea el índice

    def __obtener_vertice_dist_mas_corta_desconocido(self,T):
        #Elijo vértice con la distancia más corta y desconocido
        dist_mas_corta = float('inf')
        for i in range(self.__cantNodos):
            if T[i].conocido == False and T[i].distancia < dist_mas_corta:
                v = i
                dist_mas_corta = T[i].distancia
        return v

    def __crear_tabla_T(self):
        #Inicializa la tabla a utilizar por el algoritmo de Dijkstra
        T = []
        for i in range(self.__cantNodos):
            registro = Registro(self.__nodos[i],False,float('inf'),None) #inf, dist mas larga posible
            T.append(registro)
        return T

    def __obtener_caminos_de_tabla_T(self,tabla_T):
        caminos = []
        for registro in tabla_T:
            caminos.append(registro.camino)
        return caminos

    def __mostrar_tabla_T(self,tabla_T):
        tabla = Table(title="Tabla T")
        tabla.add_column("Vértices", style="green")
        tabla.add_column("Conocido")
        tabla.add_column("Distancia")
        tabla.add_column("Camino")

        for i in range(len(tabla_T)):
            tabla.add_row("{}".format(i),
                    "{}".format(tabla_T[i].conocido),
                    "{}".format(tabla_T[i].distancia), 
                    "{}".format(tabla_T[i].camino))
        print(tabla)

    def mostrarNodos(self):
        print(self.__nodos)

    def mostrar_relaciones(self):
        print(self.__arreglo)
     
    def __reconstruir_camino(self,nodo_destino,predecesores):
        #Reconstruyo el camino a partir del nodo destino mirando los predecesores
        camino = []
        nodo = nodo_destino
        while nodo != None:
            camino.append(nodo)
            nodo = predecesores[nodo]
        
        #Doy vuelta el camino para mostrar desde nodo inicial a nodo destino
        camino.reverse()
        return camino
