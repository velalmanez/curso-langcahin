from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

chat = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.7)

plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.\nNombre del usuario: {nombre}.\nAsistente:"
)

chain = LLMChain(llm=chat, prompt=plantilla) # Crear la cadena LLMChain con el modelo y la plantilla

respuesta = chain.run("Aleks") # Ejecutar la cadena con el nombre "Carlos"
print(respuesta) # Imprimir la respuesta generada por el modelo