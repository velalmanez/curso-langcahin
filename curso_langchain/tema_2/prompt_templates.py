from langchain_core.prompts import PromptTemplate

template = "Eres un experto en marketing, sugiere un eslogan creativo para un producto {producto}"

prompt = PromptTemplate(
    template = template,
    input_variables= ["producto"]
)

# Ver la plantilla armada antes de pasarla al LLM
prompt_lleno = prompt.format(producto = "consola de videojugos")
print(prompt_lleno)