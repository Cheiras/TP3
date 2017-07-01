import random
import sys
import heapq
from TDAs import *


def procesar_archivo(grafo, archivo):
	"""Función que abre el archivo y linea por linea va generando vertices y aristas."""
	lineas_de_cabecera = 3
	try:
		with open(archivo, "r") as archivo:
			i = 0
			for linea in archivo:
				if (i <= lineas_de_cabecera):
					i += 1
					continue
				id_1, id_2 = linea.rstrip("\n").split("\t")
				vertice_1 = Vertice(id_1, id_1)
				vertice_2 = Vertice(id_2, id_2)
				grafo.agregar_vertice(vertice_1)
				grafo.agregar_vertice(vertice_2)
				grafo.agregar_arista(vertice_1, vertice_2)
	except FileNotFoundError:
		print("El archivo no fue creado aún.")
		return False
	except IOError:
		print("Error al intentar abrir o guardar el archivo.")
		return False
	return True

def generar_grafo(archivo):
	"""Función que crea un grafo y le agrega todos los vertices y aristas."""
	grafo = Grafo()
	if not procesar_archivo(grafo, archivo):
		return False
	return grafo

def get_rand_vert(lista):
	"""Devuelve una clave aleatoria del diccionario.
	Pre: El diccionario no esta vacio"""
	posicion = random.randint(0, len(lista)-1)
	return lista[posicion]

def validar_vertice(vertice, grafo):
	"""Verifica si el vértice se encuentra en el grafo."""
	if vertice == -1:
		print("El vertice no se encuentra en el grafo.")
		return False
	return True

def validar_cantidad(cantidad, grafo):
	"""Verifica que el numero pasado por parametro esté dentro del rango del grafo."""
	return cantidad < grafo.cantidad_vertices()

def verificar_elecciones(vertice, n, grafo):
	"""Verifica las elecciones pasadas por parametro."""
	if not validar_cantidad(n, grafo):
		print("Ingreso una cantidad mayor a la del grafo.")
		return False
	return validar_vertice(vertice, grafo)

def establecer_cantidad(n, grafo):
	"""Establece la cantidad de random walks a hacer según el numero pasado por parametro."""
	cantidad = n*100
	if not validar_cantidad(cantidad, grafo):
		cantidad = grafo.cantidad_vertices()
	return cantidad

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

def crear_heap_menores(diccionario, largo):
	"""Genera un heap de menores de largo dado lleno de vertices similares 
	al recibido por parametro."""
	heap_min = []
	heapq.heapify(heap_min)
	for vertice in list(diccionario.keys()):
		tupla = (diccionario[vertice], vertice)
		if len(heap_min) < largo:
			heapq.heappush(heap_min, tupla)
		else:
			if heap_min[0][0] < tupla[0]:
				heapq.heapreplace(heap_min,tupla)
	return heap_min

def recorrido_BFS(grafo, origen, destino):
	"""Hace recorrido BFS desde un origen hasta un destino si se desea agregarle."""
	visitados = {}
	padre = {}
	orden = {}
	padre[origen] = None
	orden[origen] = 0
	q = Cola()
	q.encolar(origen)
	visitados[origen] = True
	while not q.esta_vacia():
		v = q.desencolar()
		vertice = grafo.obtener_vertice(v)
		for w in grafo.adyacentes_vertice(vertice):
			if w not in visitados:
				visitados[w] = True
				padre[w] = v
				orden[w] = orden[v] + 1
				if(destino != None ):
					if(w == destino):
						break;
				q.encolar(w)
	return padre, orden

def verificar_parametros(comando, ingreso):
	"""Verifica que los parametros ingresados por el usuario sean correctos."""
	if len(ingreso) == 0 or len(ingreso) > 3:
		print("Ingresó una cantidad incorrecta de parametros.")
		return False
	if (comando == 0):
		print("El comando ingresado es incorrecto.")
		return False
	if (comando == 1 or comando == 2 or comando == 3):
		if (len(ingreso) != 3):
			print("Ingresó una cantidad incorrecta de parametros.")
			return False
	if (comando == 4 or comando == 5):
		if (len(ingreso) != 2):
			print("Ingresó una cantidad incorrecta de parametros.")
			return False
	if (comando == 6 or comando == 7 or comando == 8):
		if (len(ingreso) != 1):
			print("Ingresó una cantidad incorrecta de parametros.")
			return False
	return True

