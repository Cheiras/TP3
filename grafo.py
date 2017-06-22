from random import *
import sys

class Vertice:
	"""Representa un vertice con operaciones ver adyacentes y agregar adyacentes."""

	def __init__(self, id, label):
		"""Crea un vertice."""
		self.id = id
		self.label = label
		self.dic_ady = {}

	def __str__(self):
		return(str(self.id))

	def adyacentes(self):
		"""Devuelve un diccionario conteniendo a todos los adyacentes a un vertice."""
		return self.dic_ady

	def agregar_adyacente(self, vertice):
		"""Agrega adyacencia entre dos vertices."""
		if vertice.id in self.adyacentes():
			return False
		self.dic_ady[vertice.id] = vertice
		vertice.dic_ady[self.id] = self

class Grafo:
	"""Representa un grafo con operaciones agregar y quitar un vertice, agregar y quitar una arista, 
	obtener adyacencias, verificar si dos vertices son adyacentes, verificar si un vertice existe,
	obtener la cantidad de vertices, obtener los identificadores del grafo e iterar.."""

	def __init__(self):
		"""Crea una grafo vacío."""
		self.vertices = {}
		self.cantidad_vert = 0
		self.cantidad_aris = 0

	def obtener_vertices(self):
		"""devuelve un diccionario con los vertices del Grafo"""
		return self.vertices

	def obtener_vertice(self,id):
		"""Devuelve el Vertice correspondiente al Identificador"""
		return self.vertices.get(id, -1)

	def agregar_vertice(self, vertice):
		"""Agrega un vertice al grafo."""
		if not vertice.id in self.vertices:
			self.vertices[vertice.id] = vertice
			self.cantidad_vert =+ 1
		
	def quitar_vertice(self,vertice):
		"""Quita un vertice del grafo"""
		if not vertice in self.vertices:
			return False
		for adyacente in vertice.adyacentes:
			self.vertices[adyacente].adyacentes.pop(vertice.id)
		self.vertices.pop(vertice.id)
		self.cantidad_vertices -= 1
		return True

	def cantidad_vertices(self):
		"""Devuelve la cantidad de vertices del grafo."""
		return self.cantidad_vert	

	def agregar_arista(self, vertice, vertice_2):
		"""Agrega una arista entre dos vertices."""
		vertice.agregar_adyacente(vertice_2)
		self.cantidad_aris += 1

	def quitar_arista(self,vertice,vertice_2):
		"""Quita una arista entre dos vertices."""
		if not vertice_2 in vertice.adyacentes:
			return False
		vertice.adyacentes.pop(vertice_2.id)
		vertice_2.adyacentes.pop(vertice.id)
		self.cantidad_aris -= 1
		return True

	def cantidad_aristas(self):
		"""Devuelve la cantidad de aristas del grafo"""
		return self.cantidad_aris

	def verificar_conexion(self,vertice,vertice_2):
		"""Verifica si dos vertices están conectados."""
		return vertice_2 in vertice.adyacentes

	def adyacentes_vertice(self, vertice):
		"""Devuelve un diccionario conteniendo todos los vertices adyacentes a uno."""
		return vertice.adyacentes

	def vertice_existe(self, vertice):
		"""Verifica si un vertice existe en un grafo."""
		return vertice in self.vertices

	#def obtener_identificadores(self):
	
	def cantidad_vertices(self):
		"""Devuelve la cantidad de vertices que tiene el grafo."""
		return len(self.vertices)



def validar_cantidad(grafo, valor):
	"""Verifica que el parametro pasado sea correcto."""
	return valor < grafo.cantidad_vertices()

def procesar_archivo(grafo, archivo):
	"""Función que abre el archivo y linea por linea va generando vertices y aristas."""
	lineas_de_cabecera = 4
	try:
		with open(archivo, "r") as archivo:
			i = 0
			for linea in archivo:
				if (i <= lineas_de_cabecera):
					i += 1
					continue
				id_1, id_2 = linea.rstrip("\n").split("\t")
				vertice_1 = Vertice(id_1, None)
				vertice_2 = Vertice(id_2, None)
				if not vertice_1 in grafo.vertices:
					grafo.agregar_vertice(vertice_1)
				if not vertice_2 in grafo.vertices:
					grafo.agregar_vertice(vertice_2)
				grafo.agregar_arista(vertice_1, vertice_2)
	except FileNotFoundError:
		print("El archivo no fue creado aún.")
	except IOError:
		print("Error al intentar abrir o guardar el archivo.")
	except ValueError:
		print("El archivo está vacío.")

def generar_grafo(archivo):
	"""Función que crea un grafo y le agrega todos los vertices y aristas."""
	grafo = Grafo()
	procesar_archivo(grafo, archivo)
	return grafo

def get_rand_key(diccionario):
	"""Devuelve una clave aleatoria del diccionario.
	 Pre: El diccionario no esta vacio"""
	for i in diccionario.keys():
		return i

def random_walk(largo, cantidad, vertice, grafo):
	"""Genera un random walk."""
	if not validar_cantidad(grafo, largo):
		return -1
	apariciones = {}
	for c in range(cantidad):
		i = 0
		while i < largo:
			w = get_rand_key(grafo.obtener_vertices())
			cant = apariciones.get(w.id, 0)
			apariciones[w.id] = cant+1  
			i += 1
			v = w
	return apariciones

def heap_similares(vertice, largo, cantidad):
	"""Genera un heap de menores de largo dado lleno de vertices similares al recibido por parametro."""
	if not validar_cantidad(grafo, largo):
		return -1
	largo = largo*10	
	if not validar_cantidad(grafo, largo):
		largo = grafo.cantidad_vertices()	
	apariciones = random_walk(largo, cantidad, vertice)
	heap_min = []
	heapq.heapify(heap_min)
	for vertice in apariciones:
		tupla = (apariciones[vertice.id], vertice.id)
		if len(heap_min) < largo:
			heapq.heappush(heap_min, tupla)
		else:
			if heap_min[0][0] < tupla[0]:
				heapq.heapreplace(heap,tupla)
	return heap_min

"""def recorrido_BFS(grafo, origen):
    visitados = {}
    padre = {}
    orden = {}
    for v in grafo:
        if v not in visitados:
            padre[v] = None
            orden[v] = 0
            q = Cola()
    		q.encolar(origen)
    		visitados[origen] = True
    		while len(cola) > 0:
		        v = cola.desencolar()
		        for w in grafo.adyacentes_vertice(v):
		            if w not in visitados:
		                visitados[w] = True
		                padre[w] = v
		                orden[w] = orden[v] + 1
		                q.encolar(w)
		    return padre, orden"""
		 


def similares(id, n, grafo):
	"""Dado un usuario, encontrar los personajes más similares a este."""
	if not validar_cantidad(grafo, n):
		return -1
	vertice = grafo.obtener_vertice(id)
	print(vertice)
	if vertice == -1:
		return False
	heap_min = heap_similares(vertice, n, 2000)
	for i in range(len(heap_min)):
		print("{}\t".format(heap_min[i][1]),end=" ")

def recomendar(id, n, grafo):
	"""Dado un usuario, recomienda otro (u otros) usuario con el cual aún no tenga relación, y sea lo más similar a él posible."""
	if not validar_cantidad(grafo, n):
		return -1 
	vertice = grafo.obtener_vertice(id)
	if vertice == -1:
		return False
	lista = []
	heap_min = heap_similares(vertice, n, 2000)
	for i in range(len(heap_min)):
		cant, vertice_aux = heapq.heappop(heap_min)
		if not vertice_aux in grafo.adyacentes_vertice(vertice):
			lista.append(vertice_aux.id)
	for c in range(len(lista)-1,-1,-1):
		print("{}\t".format(lista[(i)]))
	#VER QUE HACEMOS SI NO IMPRIME SUFICIENTE

def camino(id_1, id_2, grafo):
	"""Busca el camino mas corto entre dos vertices."""
	vertice_1 = grafo.obtener_vertice(id)
	if vertice_1 == -1:
		return False
	vertice_2 = grafo.obtener_vertice(id)
	if vertice_2 == -1:
		return False	
	lista_camino = []
	padre = vertice_2.id
	lista_camino.append(vertice_2.id)
	for i in range(len(camino)):
		padre = camino[padre]
		lista_camino.append(padre)
	for i in range(len(camino),-1,-1):
		print ("{}\t".format(camino[i]))

def centralidad(n, grafo):
	if not validar_cantidad(grafo, n):
		return -1
	heap = []
	heapq.heapify(heap)
	for vertice in grafo.obtener_vertices():
		a = 0
		if a == n*10:
			break
		a += 1	
		heap_min = heap_similares(vertice, n, 1000)
		for i in range(len(heap_min)):
			if len(heap) < n:
				heapq.heappush(heap, heapq.heappop(heap_min))
			else:
				if heap[0][0] < heap_min[0][0]:
					heapq.heapreplace(heap,heapq.heappop(heap_min))

"""def distancias(id, grafo):
	vertice = grafo.obtener_vertice(id)
	if vertice == -1:
		return False
	camino, distancia = recorrido_BFS(grafo, vertice)
	lista_distancias = []
	for vertice in distancia:
	obtengo distancia maxima
	for i in range distancia_maxima
		lista.append(0)
	for vertice in distancia:
		lista[distancia[vertice]] += 1
	for i in range(len(lista)):
		print("Distancia {}: {}",format(i,lista[i]))"""

def estadisticas(grafo):
	acumulador = 0
	for vertice in grafo.vertices:
		vertice = grafo.obtener_vertice(id)
		acumulador += len(grafo.adyacentes_vertice(vertice))
	promedio = acumulador/len(grafo.vertices)
	cant_aristas = grafo.cantidad_aris()
	cant_vertices = grafo.cantidad_aris()
	densidad = cant_vertices/cant_aristas
	print("Estadisticas:")
	print("Cantidad de Vertices: {} ".format(cant_vertices))
	print("Cantidad de Aristas: {}".format(cant_aristas))
	print("Densidad del Grafo: {} ".format(densidad))
	print("Promedio de grado de entrada de cada vértice: {}".format(promedio))

def main():
	"""Función que corre el programa."""
	archivo = input("Ingrese el nombre del archivo: ")
	grafo = generar_grafo(archivo)
	#for vertice in grafo.obtener_vertices():
	#	print(vertice.adyacentes())
	estadisticas(grafo)

main()



#USAR validar_cantidad
#DOCUMENTAR TODO
#AGREGAR FUNCION CHEQUEAR VERTICE
#NO USAR VERTICE ADYACENTES SINO GRAFO.ADYANCENTES(V)
#VERIFICAR DATOS INGRESADOS PARA SIMILARES Y RECOMENDAR
#ESTO, ES ASI? GRAFO.VERTICES(),ETC























