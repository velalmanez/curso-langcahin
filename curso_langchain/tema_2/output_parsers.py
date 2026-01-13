from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI  


class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto proporcionado.")
    sentimiento: str = Field(description="Sentimiento predominante del texto (positivo, negativo, neutral).")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.6)

structured_llm = llm.with_structured_output(AnalisisTexto)

texto_prueba = "El producto es excelente y el servicio al cliente fue muy atento."

respuesta = structured_llm.invoke(f"Analiza el siguiente texto: {texto_prueba}")

respuesta_json = respuesta.model_dump_json()

print(respuesta_json)