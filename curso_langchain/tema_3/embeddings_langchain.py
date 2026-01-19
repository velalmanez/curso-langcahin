from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np

embedings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

texto_1 = "LangChain es una biblioteca de Python que facilita la creación de aplicaciones impulsadas por modelos de lenguaje."
texto_2 = "Los embeddings son representaciones vectoriales de texto que capturan el significado semántico."

vec1 = embedings.embed_query(texto_1)
vec2 = embedings.embed_query(texto_2)

cos_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

print(f"Similitud coseno entre los dos textos: {cos_similarity:.4f}")