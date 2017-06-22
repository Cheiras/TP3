#include "cola.h"
#include <stdlib.h>

typedef struct nodo{
	void* datos;
	struct nodo* prox;
}nodo_t;

typedef struct cola{
	nodo_t* primer_nodo;
    nodo_t* ult_nodo;
}cola_t;

/********************************************/

cola_t* cola_crear(void){
	cola_t* cola = (cola_t*) malloc(sizeof(cola_t));
	if (cola == NULL) return NULL;
	cola->primer_nodo = NULL;
	cola->ult_nodo = NULL;
	return cola;
}

bool cola_esta_vacia(const cola_t *cola){
	return (cola->primer_nodo == NULL);
	}

bool cola_encolar(cola_t *cola, void* valor){ 
	nodo_t* nuevo_nodo = malloc(sizeof(nodo_t));
	if (nuevo_nodo == NULL) return false;
	nuevo_nodo->datos = valor;
	nuevo_nodo->prox = NULL;

	if(cola->primer_nodo == NULL){
		cola->primer_nodo = nuevo_nodo;
		cola->ult_nodo = nuevo_nodo;	
	}
	else{
		cola->ult_nodo->prox = nuevo_nodo;
		cola->ult_nodo = nuevo_nodo;
	}
	return true;
}

void* cola_ver_primero(const cola_t *cola){
	if(cola->primer_nodo == NULL) return NULL;
	return cola->primer_nodo->datos;
}

void* cola_desencolar(cola_t *cola){
	if (cola->primer_nodo == NULL) return NULL;
	void* valor = cola->primer_nodo->datos;
	nodo_t* aux = cola->primer_nodo->prox;
	free(cola->primer_nodo);
	cola->primer_nodo = aux;
	return valor;
}



void cola_destruir(cola_t *cola, void destruir_dato(void*)){
	nodo_t* nodo = cola->primer_nodo;
	while(nodo){
		if(destruir_dato != NULL){
			destruir_dato(nodo->datos);
		}
		nodo_t* aux = nodo->prox;	
		free(nodo);
		nodo = aux;
	}
	free(cola);
}