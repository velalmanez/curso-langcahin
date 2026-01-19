from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader #Cargar multiples PDFs de un directorio
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Caragar documentos desde un directorio de PDFs 
loader = PyPDFDirectoryLoader("G:\\TRABAJO\\CURSOS\\curso-langcahin\\curso_langchain\\tema_3\\contratos")
documents = loader.load()

print(f"Número de documentos cargados: {len(documents)} documentos desde el directorio.")

# configura el tamaño de los chunks de texto
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

# crear los chunks de texto
docs_split = text_splitter.split_documents(documents)
print(f"Número de documentos después del split: {len(docs_split)} chunks de texto.")



vector_store = Chroma.from_documents(
    documents=docs_split,
    embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
    persist_directory="G:\\TRABAJO\\CURSOS\\curso-langcahin\\curso_langchain\\tema_3\\vector_store_contratos"
)

consulta = "¿Cuáles son las obligaciones principales del arrendatario según el contrato de arrendamiento?"

#Hacer busqueda por similitud
resultados = vector_store.similarity_search(consulta, k=3) # obtiene los 3 fragmentos más relevantes

print("Resultados de la búsqueda por similitud:")
for i, doc in enumerate(resultados, start=1):
    print(f"contenido: {doc.page_content}")
    print(f"metadatos: {doc.metadata}")