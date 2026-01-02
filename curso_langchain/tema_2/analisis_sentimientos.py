from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
import json

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


def preprocess_text(text):
    """limpia el texto y limita su longitud a 500 caracteres"""
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

#Generador de resumen
def generate_summary(text):
    prompt = f"Resume en una sola oracion:{text}"
    response = llm.invoke(prompt)
    return response.content

summary_branch = RunnableLambda(generate_summary)

def analyze_sentiment(text):
    prompt = f"""Analiza el sentimineto del siguiente texto.
    Responde UNICAMENTE en formato de JSON valido:
    {{"sentimiento": "positivo|neutro", "razon": "Justificacion breve"}}

    Texto: {text}"""
    response = llm.invoke(prompt)
    try:
       return json.loads(response.content)
    except json.JSONDecodeError:
         return {"sentimiento": "uknow", "razon": "No se pudo analizar el sentimiento"}

sentiment_branch = RunnableLambda(analyze_sentiment)

def merge_results(data):
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }


merger = RunnableLambda(merge_results)

parallel_analysis = RunnableParallel({
    "resumen": summary_branch, # se asocia el objeto runnable previamente creado
    "sentimiento_data": sentiment_branch

})

# cadena completa
chain = preprocessor | parallel_analysis | merger

# conjunto de reseñas
reviews_batch = [
    "Me encantó el producto, superó mis expectativas y el servicio fue excelente.",
    "El producto está bien, pero el envío tardó demasiado tiempo.",
    "No estoy satisfecho con la calidad del producto, esperaba algo mejor."
]

# ejecuta la cadena en modo batch, manejando varias reseñas a la vez con un procesamiento en paralelo 
resultado_batch = chain.batch(reviews_batch)

print(resultado_batch)