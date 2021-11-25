import numpy as np
from .claseColas import ColaEncadenada
from rich.table import Table
from rich import print

class Nodo:
    def __init__(self,dato=None):
        self.__dato = dato
    
    def getDato(self):
        return self.__dato
    def setDato(self,dato):
        self.__dato = dato

class Registro:
    def __init__(self,nodo,conocido,distancia,camino):
        self.nodo = nodo
        self.conocido = conocido
        self.distancia = distancia
        self.camino = camino

   
class DigrafoSecuencial:
    '''Digrafo con Representación Secuencial, ponderado o no'''

    def __init__(self,cant_nodos,ponderado=False):
        self.__cantNodos = cant_nodos
        self.__ponderado = ponderado

        #Se trabaja con una matriz de orden nxn
        #Si es ponderado se carga con datos, sino con 0 o 1 (adyacencia)
        self.__matriz = np.full((self.__cantNodos,self.__cantNodos),0)
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
            self.__matriz[i][j] = peso
        except ValueError as error:
            print(error)
 
    def adyacentes(self,i):
        '''Determina los nodos adyacentes del nodo ingresado'''
        nodos_adyacentes = []
        try:
            self.__validar_indices(i)
            for j in range(self.__cantNodos):
                if self.__matriz[i][j] > 0: #si tiene peso puede ser mayor a 1
                    nodos_adyacentes.append(j)
        except ValueError as error:
            print(error)
        return nodos_adyacentes

    def grado(self,nodo):
        '''Retorna el grado de salida (número de aristas que empiezan en el nodo) y el grado de entrada (número de aristas que terminan en el nodo'''
        adyacentes = self.adyacentes(nodo)

        grado_salida = len(adyacentes)
        grado_entrada = 0
        for i in range(self.__cantNodos):
            if i != nodo:
                adyacentes_a_i = self.adyacentes(i)
                if nodo in adyacentes_a_i:
                    grado_entrada += 1
        return grado_salida,grado_entrada
 
    def camino(self,nodo_inicial,nodo_destino,mostrar_camino=False):
        """Aplica búsqueda en profundidad para encontrar un camino (no necesariamente el mínimo)"""
        camino = []
        try:
            self.__validar_indices(nodo_inicial,nodo_destino)
            datos = self.busqueda_en_profundidad_REP(nodo_inicial)
            predecesores = datos[1]
            camino = self.__reconstruir_camino(nodo_destino,predecesores)
            if mostrar_camino:
                print("Camino desde {} a {}: {}".format(nodo_inicial,nodo_destino,camino))
        except ValueError as error:
            print(error)
        return camino
  
    def camino_minimo(self,nodo_inicial,nodo_destino,mostrar_mensaje = False):
        '''Si es ponderado busca el camino con el menor peso total, aplica Floyd, sino REA, camino con menor numero de aristas'''
        camino = []
        try: 
            self.__validar_indices(nodo_inicial,nodo_destino)
            if self.__ponderado:
                Q, siguientes = self.algoritmo_Floyd()
                nodo = nodo_inicial
                while nodo != nodo_destino:
                    camino.append(nodo)           
                    nodo = siguientes[nodo][nodo_destino]
                camino.append(nodo_destino)         
            else:
                datos = self.busqueda_en_amplitud_REA(nodo_inicial)
                predecesores = datos[2]
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
            nodos_visitados = datos[1] #Nodos visitados
            if False in nodos_visitados:
                es_conexo = False
            i+=1
        return es_conexo

    def aciclico(self):
        '''Evalua si el grafo tiene ciclos o no, aplica Warshal si no es ponderado, Floyd si es ponderado'''
        #Ciclo: camino simple (todos los nodos son distintos, salvo v0 y vn) cerrado de longitud 3 o mas
        es_aciclico = True   
        
        #Analizo las diagonales del las matrices para determinar si hay o no ciclos
        if self.__ponderado:
            relaciones,_ = self.algoritmo_Floyd()
        else:
            relaciones = self.algoritmo_Warshall()
        i = 0
        #Analizo la diagonal, si hay al menos 1 uno tiene un ciclo y no es aciclico
        while i < self.__cantNodos and es_aciclico:
            if self.__ponderado and relaciones[i][i] != np.inf:
                es_aciclico = False
            elif not self.__ponderado and relaciones[i][i] == 1:
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
                        if self.__matriz[v][w] < T[w].distancia:
                            T[w].distancia = self.__matriz[v][w]
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
        nodos_visitados[nodo_origen] = True #marcar el origen

        cola.insertar(nodo_origen)
        while not cola.vacia():
            nodo_v = cola.suprimir()
            recorrido.append(nodo_v)
            nodos_u = self.adyacentes(nodo_v)

            for u in nodos_u:
                if nodos_visitados[u] == False:
                    nodos_visitados[u] = True #marcar u
                    predecesores[u] = nodo_v #Guardo el predecesor
                    cola.insertar(u)
        
        datos = [recorrido, nodos_visitados, predecesores]
        return datos
    
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
        datos = [recorrido,predecesores,nodos_visitados]
        return datos

    def algoritmo_Warshall(self):
        '''Determina la existencia de caminos en grafos dirigidos no ponderados'''
        #Matriz de caminos
        P = np.copy(self.__matriz)
        for k in range(self.__cantNodos):
            for i in range(self.__cantNodos):
                for j in range(self.__cantNodos):
                    P[i][j] =  P[i][j] or (P[i][k] and P[k][j])         
        return P

    def algoritmo_Floyd(self):
        '''Determina caminos mínimos en grafos dirigidos ponderados'''
        #Matriz de caminos mínimos
        Q = np.full((self.__cantNodos,self.__cantNodos),np.inf)
        #en cada fila el nodo del que parto, en columnas, el nodo al que intenta llegar
        #El valor indica el siguiente nodo partida, irse moviendo por la matriz hasta llegar al nodo destino
        siguientes = np.full((self.__cantNodos,self.__cantNodos),0)

        for i in range(self.__cantNodos):
            for j in range(self.__cantNodos):
                if self.__matriz[i][j] != 0:
                    Q[i][j] = self.__matriz[i][j]
                    siguientes[i][j] = j

        for k in range(self.__cantNodos):
            for i in range(self.__cantNodos):
                for j in range(self.__cantNodos):
                    suma = Q[i][k] + Q[k][j]
                    if suma < Q[i][j]:
                        Q[i][j] = int(suma)
                        siguientes[i][j] = siguientes[i][k]
        return Q, siguientes      
    
    #------------------------#
    #   METODOS AUXILIARES   #
    #------------------------#
 
    def __validar_indices(self,i,j=0):
        #Lanza una excepción en caso de índices no validos
        if i < 0 or j < 0 or i >= self.__cantNodos or j >= self.__cantNodos:
            raise ValueError('Indices no válidos')
   
    def __obtener_vertice_dist_mas_corta_desconocido(self,T):
        #Elijo vértice con la distancia más corta y desconocido
        dist_mas_corta = float('inf')
        i=0
        while i < self.__cantNodos:
            if T[i].conocido == False and T[i].distancia < dist_mas_corta:
                v = i
                dist_mas_corta = T[i].distancia
            i+=1
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
        print(self.__matriz)
     
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