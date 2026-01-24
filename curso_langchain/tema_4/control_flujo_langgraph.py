from typing import TypedDict
from langgraph.graph import StateGraph, START, END

#Definir el estado
class State(TypedDict):
    numero: int
    result: str

graph = StateGraph(State)

# Definirt los nodos 
def caso_par(state):
    return{'result': 'El numero es par'}

def caso_impar(state):
    return{'result': 'El numero es impar'}

graph.add_node("Par", caso_par)
graph.add_node("Impar", caso_impar)

# Definir la funcion de routing para decidir la rama de ejecucuion 
def decidir_rama(state):
    if state["numero"] % 2 == 0:
        return "Par"    # Nombre del nodo
    else:
        return "Impar" # Nombre del nodo
    
# añadir el routing al grafo
graph.add_conditional_edges(START, decidir_rama)

# conectar ambo casos
graph.add_edge("Par", END)
graph.add_edge("Impar", END)

compiled  = graph.compile()

#Probar el grafo condicional
print(compiled.invoke({"numero": 3})["result"])