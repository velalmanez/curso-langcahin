from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. definicion de esquema del estado
class State(TypedDict):
    texto_original: str
    texto_mayus: str
    longitud: int

# 2. creacion del grafo de estado
graph = StateGraph(State)

# 3. definicion de las funciones de los nodos 
def poner_mayuscula(state):
    texto = state['texto_original']
    return {"texto_mayus": texto.upper()}

def contar_caracteres(state): 
    texto = state['texto_mayus']
    return {"longitud": len(texto)}

# 4. Añadir los nodos al grafo
graph.add_node("Mayus", poner_mayuscula)
graph.add_node("Contar", contar_caracteres)

# 5. conectar los nodos en secuencia (flujo de ejecuion)
graph.add_edge(START, "Mayus") # pasa el estado al nodo Mayus
graph.add_edge("Mayus", "Contar") # pasa del nodo Mayus a Contar
graph.add_edge("Contar", END) # pasa del nodo Contar al nodo final

# 6. Compilar el grafo
compiled_graph = graph.compile() 

# 7. Invocar el grafo con estado inicial 
estado_inicial = {"texto_original": "Hola Mundo"}
resultado = compiled_graph.invoke(estado_inicial)
print(resultado)