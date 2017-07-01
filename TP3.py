import random
import sys
import heapq
import time
from TDAs import *
from funciones_aux import *

def similares(iden, n, grafo):
	"""Dado un usuario, encontrar los personajes más similares a este."""
	LARGO_RAN_WALKS = 30
	vertice = grafo.obtener_vertice(iden)
	if not verificar_elecciones(vertice, n, grafo):
		return False
	cantidad = establecer_cantidad(n, grafo)
	apariciones = random_walk(cantidad, LARGO_RAN_WALKS, vertice, grafo)
	heap_min = crear_heap_menores(apariciones, n, iden)
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
	heap_min = crear_heap_menores(apariciones, n*2, iden)
	i = 0
	lista = []
	for i in range(len(heap_min)):
		cant, vertice_aux = heapq.heappop(heap_min)
		if not vertice_aux in list(grafo.adyacentes_vertice(vertice).keys()):
			lista.append(vertice_aux)
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
	CANT_RAN_WALKS = 100
	LARGO_RAN_WALKS = 3
	FACTOR_DE_CENTRALIDAD = 50
	globales = {}
	for i in range(n*FACTOR_DE_CENTRALIDAD):
		vertice = random.choice(grafo.obtener_vertices())
		apariciones = random_walk(CANT_RAN_WALKS, LARGO_RAN_WALKS, vertice, grafo)	
		for vertice in apariciones.keys():
			apariciones = globales.get(vertice, 0) + 1
			globales[vertice] = apariciones
	heap = crear_heap_menores(globales, n, None)
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
			comunidades(grafo)
		if(comando == 8):
			sys.exit()

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