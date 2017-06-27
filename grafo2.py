import random
import sys
import heapq

class Vertice:
	"""Representa un vertice con operaciones ver adyacentes y agregar adyacentes."""
	
	def __init__(self, iden, label):
		"""Crea un vertice."""
		self.iden = iden
		self.label = label
		self.dic_ady = {}

	#def __repr__(self):
	#	return self.iden

	def adyacentes(self):
		"""Devuelve un diccionario conteniendo a todos los adyacentes a un vertice."""
		return self.dic_ady

	def agregar_adyacente(self, vertice):
		"""Agrega adyacencia entre dos vertices."""
		if not vertice.iden in self.dic_ady:
			self.dic_ady[vertice.iden] = vertice
			return True

class Grafo:
	"""Representa un grafo con operaciones agregar y quitar un vertice, agregar y quitar una arista, 
	obtener adyacencias, verificar si dos vertices son adyacentes, verificar si un vertice existe,
	obtener la cantidad de vertices, obtener los identificadores del grafo e iterar.."""

	def __init__(self):
		"""Crea una grafo vacío."""
		self.vertices = {}
		self.cantidad_vert = 0
		self.cantidad_aris = 0

	def obtener_dic_iden(self):
		"""Devuelve un diccionario con los vertices del Grafo"""
		return self.vertices

	def obtener_vertice(self, iden):
		"""Devuelve el Vertice correspondiente al Identificador"""
		return self.vertices.get(iden, -1)

	def agregar_vertice(self, vertice):
		"""Agrega un vertice al grafo."""
		if not vertice.iden in self.vertices:
			self.vertices[vertice.iden] = vertice
			self.cantidad_vert += 1
			return True
		
	def quitar_vertice(self,vertice):
		"""Quita un vertice del grafo"""
		if not vertice in self.vertices:
			return False
		for adyacente in vertice.adyacentes:
			self.vertices[adyacente].adyacentes.pop(vertice.iden)
		self.vertices.pop(vertice.iden)
		self.cantidad_vertices -= 1
		return True

	def cantidad_vertices(self):
		"""Devuelve la cantidad de vertices del grafo."""
		return self.cantidad_vert()	

	def agregar_arista(self, vertice, vertice_2):
		"""Agrega una arista entre dos vertices."""
		if vertice.iden in self.vertices:
			vertice = self.vertices.get(vertice.iden, -1)
		if vertice_2.iden in self.vertices:
			vertice_2 = self.vertices.get(vertice_2.iden, -1)
		if vertice.agregar_adyacente(vertice_2) and vertice_2.agregar_adyacente(vertice):
			self.cantidad_aris += 1

	def quitar_arista(self,vertice,vertice_2):
		"""Quita una arista entre dos vertices."""
		if not vertice_2 in vertice.adyacentes:
			return False
		vertice.adyacentes.pop(vertice_2.iden)
		vertice_2.adyacentes.pop(vertice.iden)
		self.cantidad_aris -= 1
		return True

	def cantidad_aristas(self):
		"""Devuelve la cantidad de aristas del grafo"""
		return self.cantidad_aris

	def verificar_conexion(self,vertice,vertice_2):
		"""Verifica si dos vertices están conectados."""
		return vertice_2 in vertice.adyacentes()

	def adyacentes_vertice(self, vertice):
		"""Devuelve un diccionario conteniendo todos los vertices adyacentes a uno."""
		return vertice.adyacentes()

	def vertice_existe(self, vertice):
		"""Verifica si un vertice existe en un grafo."""
		return vertice in self.vertices

	def obtener_identificadores(self):
		"""Devuelve todos los identificadores del grafo."""
		return list(self.vertices.keys())
	
	def obtener_vertices(self):
		"""Devuelve todos los identificadores del grafo."""
		return list(self.vertices.values())

	def cantidad_vertices(self):
		"""Devuelve la cantidad de vertices que tiene el grafo."""
		return self.cantidad_vert

##########################################################################################
##########################################################################################
##########################################################################################

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
				grafo.agregar_vertice(vertice_1)
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

def get_rand_vert(lista):
	"""Devuelve una clave aleatoria del diccionario.
	Pre: El diccionario no esta vacio"""
	posicion = random.randint(0, len(lista)-1)
	return lista[posicion]

def validar_cantidad(cantidad, grafo):
	return cantidad < grafo.cantidad_vertices()

def random_walk(largo, cantidad, vertice, grafo):
	"""Genera un random walk."""
	if not validar_cantidad(largo, grafo):
		return -1
	apariciones = {}
	v = vertice
	for c in range(cantidad):
		i = 0
		while i < largo:
			w = get_rand_vert(list(grafo.adyacentes_vertice(v).values()))
			cant = apariciones.get(w.iden, 0)
			apariciones[w.iden] = cant+1  
			i += 1
			v = w
	return apariciones

def heap_similares(vertice, largo, cantidad, grafo):
	"""Genera un heap de menores de largo dado lleno de vertices similares al recibido por parametro."""
	cantidad = cantidad*10	
	if not validar_cantidad(cantidad, grafo):
		cantidad = grafo.cantidad_vertices()	
	apariciones = random_walk(largo, cantidad, vertice, grafo)
	heap_min = []
	heapq.heapify(heap_min)
	for vertice in list(apariciones.keys()):
		vertice = grafo.obtener_vertice(vertice)
		tupla = (apariciones[vertice.iden], vertice.iden)
		if len(heap_min) < largo:
			heapq.heappush(heap_min, tupla)
		else:
			if heap_min[0][0] < tupla[0]:
				heapq.heapreplace(heap_min,tupla)
	return heap_min

def similares(iden, n, grafo):
	"""Dado un usuario, encontrar los personajes más similares a este."""
	if not validar_cantidad(n, grafo):
		return -1
	vertice = grafo.obtener_vertice(iden)
	if vertice == -1:
		print("El vertice no se encuentra en el grafo.")
		return False
	heap_min = heap_similares(vertice, n, 2000, grafo)
	for i in range(len(heap_min)):
		print("{} ".format(heap_min[i][1]),end=" ")
	print("\n")

def estadisticas(grafo):
	acumulador = 0
	for vertice in grafo.obtener_vertices():
		acumulador += len(grafo.adyacentes_vertice(vertice))
	promedio = acumulador/grafo.cantidad_vertices()
	densidad = grafo.cantidad_vertices()/grafo.cantidad_aristas()
	print("Estadisticas:")
	print("Cantidad de Vertices: {} ".format(grafo.cantidad_vertices()))
	print("Cantidad de Aristas: {}".format(grafo.cantidad_aristas()))
	print("Densidad del Grafo: {} ".format(densidad))
	print("Promedio de grado de entrada de cada vértice: {}".format(promedio))	

def main():
	"""Función que corre el programa."""
	archivo = input("Ingrese el nombre del archivo: ")
	grafo = generar_grafo(archivo)
	estadisticas(grafo)
	similares("1", 5, grafo)

main()