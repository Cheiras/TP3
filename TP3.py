import random
import sys
import heapq
import time
from TDAs import *

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

def menu(grafo):
	"""Corre el menú que interactúa con el usuario."""
	opciones = {"similares":1, "recomendar":2, "camino":3, "centralidad":4, "distancias":5, "estadisticas":6, "comunidades":7, "s":8}
	while True:
		ingreso = input("Ingrese el comando deseado o 'S' para salir: ").split(" ")
		comando = opciones.get(ingreso[0].lower(), 0)
		if not verificar_parametros(comando, ingreso):
			menu(grafo)
		for i in range (len(ingreso)-1, 0, -1):
			parametro = ingreso[i]
			if not parametro.isdigit():
				print("Los parametros deben ser dígitos.")
				menu(grafo)
		if(comando == 1):
			similares(ingreso[1], int(ingreso[2]), grafo)
		if(comando == 2):
			recomendar(ingreso[1], int(ingreso[2]), grafo)
		if(comando == 3):
			camino(ingreso[1], ingreso[2], grafo)
		if(comando == 4):
			centralidad(grafo, int(ingreso[1]))
		if(comando == 5):
			distancia(grafo, ingreso[1])
		if(comando == 6):
			estadisticas(grafo)
		if(comando == 7):
			ini = time.time()
			comunidades(grafo)
			fin = time.time()
			print("Tiempo:", (fin-ini))
		if(comando == 8):
			sys.exit()

##########################################################################################

def similares(iden, n, grafo):
	"""Dado un usuario, encontrar los personajes más similares a este."""
	LARGO_RAN_WALKS = 30
	vertice = grafo.obtener_vertice(iden)
	if not verificar_elecciones(vertice, n, grafo):
		return False
	cantidad = establecer_cantidad(n, grafo)
	apariciones = random_walk(cantidad, LARGO_RAN_WALKS, vertice, grafo)
	heap_min = crear_heap_menores(apariciones, n)
	for i in range(len(heap_min)):
		print("{} ".format(heap_min[i][1]),end=" ")
	print("\n")

def recomendar(iden, n, grafo):
	"""Dado un usuario, recomienda otro (u otros) usuario con el cual aún no tenga relación,
	 y sea lo más similar a él posible. Si la cantidad de similares < n, imprime la cantidad maxima."""
	LARGO_RAN_WALKS = 30
	vertice = grafo.obtener_vertice(iden)
	if not verificar_elecciones(vertice, n, grafo):
		return False
	cantidad = n*100
	cantidad = establecer_cantidad(n, grafo)
	apariciones = random_walk(cantidad, LARGO_RAN_WALKS, vertice, grafo)
	heap_min = crear_heap_menores(apariciones, n*2)
	i = 0
	lista = []
	while(i < n):
		cant, vertice_aux = heapq.heappop(heap_min)
		if not vertice_aux in list(grafo.adyacentes_vertice(vertice).keys()):
			lista.append(vertice_aux)
			i += 1
	for c in range(len(lista)-1,-1,-1):
		print("{} ".format(lista[(c)]),end=" ")
	print("\n")
	
def camino(id_1, id_2, grafo):
	"""Busca el camino mas corto entre dos vertices."""
	vertice = grafo.obtener_vertice(id_1)
	vertice_2 = grafo.obtener_vertice(id_2)
	if vertice == -1 or vertice_2 == -1:
		print("Algún vertice no se encuentra en el grafo.")
		return False
	padre, orden = recorrido_BFS(grafo, id_1, id_2)
	camino = []
	v = id_2
	while padre[v] != None:
		camino.append(v)
		v = padre[v]
	camino.append(id_1)
	print("Camino: ",end="")
	for i in range(len(camino)-1):
		print("{}->".format(camino[len(camino)-1-i]),end="")
	print("{}".format(id_2))

def centralidad(grafo, n):
	"""Obtiene lo "n" vertices con mayor influencia del grafo utilizando random walks."""
	CANT_RAN_WALKS = 10
	LARGO_RAN_WALKS = 5
	FACTOR_DE_CENTRALIDAD = 50
	globales = {}
	for i in range(n*FACTOR_DE_CENTRALIDAD):
		vertice = random.choice(grafo.obtener_vertices())
		apariciones = random_walk(CANT_RAN_WALKS, LARGO_RAN_WALKS, vertice, grafo)	
		for vertice in apariciones.keys():
			apariciones = globales.get(vertice, 0) + 1
			globales[vertice] = apariciones
	heap = crear_heap_menores(globales, n)
	for i in range(len(heap)):
		print("{} ".format(heap[i][1]),end=" ")
	print("\n")

def distancia(grafo, iden):
	"""Obtiene la cantidad de elementos que hay para cada distancia del vertice ingresado."""
	padre, orden = recorrido_BFS(grafo, iden, None)
	distancias = {}
	for vertice in orden.keys():
		if(orden[vertice] == 0):
			continue
		if not orden[vertice] in distancias:
			distancias[orden[vertice]] = []
		distancias[orden[vertice]].append(vertice)
	lista = list(distancias.keys())
	lista.sort()
	for i, elemento in enumerate(lista):
		print("Distancia {}: {}".format(elemento, len(distancias[elemento])))

def estadisticas(grafo):
	"""Imprime por pantalla las estadisticas del grafo."""
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

def comunidades(grafo):
	comunidades_d = {}
	for i in range(5):
		for vertice in grafo.obtener_vertices():
			labels = {}
			mas_aparece = 0
			label_mas_presente = 0
			for adyacente in list(grafo.adyacentes_vertice(vertice).values()):
				apariciones = labels.get(adyacente.label, 0)
				labels[adyacente.label] = apariciones + 1
			for label in labels:
				if labels[label] > mas_aparece:
					mas_aparece = labels[label]
					label_mas_presente = label
			vertice.label = label_mas_presente

	comunidades_d = {}
	for vertice in grafo.obtener_vertices():
		lista = comunidades_d.get(vertice.label, [])
		lista.append(vertice.iden)
		comunidades_d[vertice.label] = lista

	cantidad = 0
	for label in comunidades_d:
		if len(comunidades_d[label]) <= 4 or len(comunidades_d[label]) > 2000:
			continue
		cantidad+=1
		print("Comunidad {}, {} integrantes: {}".format(label, len(comunidades_d[label]),comunidades_d[label]))
	print("Cantidad de comunidades: {}".format(cantidad))


def main():
	"""Función que corre el programa."""
	archivo = input("Ingrese el nombre del archivo: ")
	print("Generando grafo.")
	grafo = generar_grafo(archivo)
	print("Grafo generado.")
	if not grafo:
		sys.exit()
	menu(grafo)

main()