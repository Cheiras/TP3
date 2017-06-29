class Vertice:
	"""Representa un vertice con operaciones ver adyacentes y agregar adyacentes."""
	
	def __init__(self, iden, label):
		"""Crea un vertice."""
		self.iden = iden
		self.label = label
		self.dic_ady = {}

	def adyacentes(self):
		"""Devuelve un diccionario conteniendo a todos los adyacentes a un vertice."""
		return self.dic_ady

	def agregar_adyacente(self, vertice):
		"""Agrega adyacencia entre dos vertices."""
		if not vertice.iden in self.dic_ady:
			self.dic_ady[vertice.iden] = vertice
			return True

class Grafo:
	"""Representa un grafo con operaciones agregar y quitar un vertice, agregar y quitar 
	una arista, obtener adyacencias, verificar si dos vertices son adyacentes, verificar
	 si un vertice existe,obtener la cantidad de vertices, obtener los identificadores
	  del grafo e iterar.."""

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
		return self.cantidad_vert

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

class Nodo:
	"""Representa un nodo."""

	def __init__(self, dato=None, prox=None):
		self.dato = dato
		self.prox = prox

	def __str__(self):
		return str(self.dato)

class Cola:
	"""Representa una cola con funciones, encolar, desencolar y está vacia."""

	def __init__(self):
		"""Crea una cola vacía."""
		self.primero = None
		self.ultimo = None 

	def encolar(self, x):
		"""Encola el elemento x."""
		nuevo = Nodo(x)
		if self.ultimo is not None:
			self.ultimo.prox = nuevo
			self.ultimo = nuevo
		else:
			self.primero = nuevo
			self.ultimo = nuevo

	def desencolar(self):
		"""Desencola el primer elemento y devuelve su valor. Si la cola está vacía, levanta ValueError."""
		if self.primero is None:
			raise ValueError("La cola está vacía")
		valor = self.primero.dato
		self.primero = self.primero.prox
		if not self.primero:
			self.ultimo = None
		return valor

	def esta_vacia(self):
		"""Devuelve True si la cola esta vacía, False si no."""
		return self.primero is None