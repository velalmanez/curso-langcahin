from langchain_core.runnables import RunnableLambda

# crear un objeto Runnable que procese un numero y devuelva un string con una funcion lambda de python
paso1 = RunnableLambda(lambda x: f"Numero recibido: {x}")

# crear un objeto runnable a partir de una funcion definida en python
def duplicar_text (texto): 
    return [texto] * 2

paso2 = RunnableLambda(duplicar_text)

# encadenar los dos runnables
pipeline = paso1 | paso2

result = pipeline.invoke(5)
print(result)  # Output: ['Numero recibido: 5', 'Numero recibido: 5']

