class ColaSecuencial:
    __items = None
    __max = 0 #Cantidad max de elementos (estructura estática)
    __pr = 0 #Apunta al primer elemento
    __ul = 0 #Apunta al ultimo elemento
    __cant = 0 #Cantidad de elementos en un momento dado

    def __init__(self,xmax):
        self.__pr = 0
        self.__ul = 0
        self.__cant = 0
        self.__max = xmax
        self.__items = []
   
    def vacia(self):
        return self.__cant == 0
 
    def llena(self):
        return self.__cant == self.__max
   
    def insertar(self,x):
        if not self.llena(): 
            self.__items.insert(self.__ul,x)
            #Para la referencia circular y que ul se ponga en 0 al llegar al final
            #Incremento usando aritmética modular
            self.__ul = (self.__ul+1)%self.__max #Dará resto 0 cuando ul+1=max
            self.__cant += 1
    
    #Suprime el primero (FIFO - primero en entrar, primero en salir)
    def suprimir(self):
        x = None
        if not self.vacia():
            x = self.__items[self.__pr]
            self.__pr = (self.__pr+1)%self.__max #Incremento usando aritmética modular
            self.__cant -= 1
        return x

class Nodo:
    __dato = None
    __sig = None

    def __init__(self,dato=0):
        self.__dato = dato
        self.__sig = None
    def setSiguiente(self,siguiente):
        self.__sig = siguiente
    def getSiguiente(self):
        return self.__sig
    def getDato(self):
        return self.__dato

class ColaEncadenada:
    __cant = 0
    __pr = None #Son de tipo Nodo
    __ul = None

    def __init__(self):
        self.__pr = None
        self.__ul = None
        self.__cant = 0

    def vacia(self):
        return self.__cant == 0
    
    #Cola dinamica, no tiene max
    def insertar(self,x):
        newNodo = Nodo(x)
        if self.vacia(): #si no hay nada ul y pr apuntan al mismo nodo
            self.__pr = newNodo
        else:
            self.__ul.setSiguiente(newNodo)
        #Para mantener el ultimo elemento
        self.__ul = newNodo
        self.__cant += 1
   
    def suprimir(self):
        x = None
        if not self.vacia():
            aux = self.__pr #Para borrar el nodo
            x = self.__pr.getDato()
            self.__pr = self.__pr.getSiguiente()
            self.__cant -= 1
            if self.__pr == None: #si el primero queda nulo, el ultimo debe quedar nulo
                self.__ul = None
            del aux
        return x
