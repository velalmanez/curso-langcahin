from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Cargar el vector store desde el directorio persistente
vector_store = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
    persist_directory="G:\\TRABAJO\\CURSOS\\curso-langcahin\\curso_langchain\\tema_3\\vector_store_contratos"
)

# convierte el vector store en un retriever: devuelve un objeto de la clase DocumentRetriever pertenciente a langchain
retriever = vector_store.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 2}
)

# definicion de consulta
consulta = "¿Donde se encuentra el local del contrato en le que participa María Jiménez Campos?"

resultados = retriever.invoke(consulta) 

print("Resultados de la búsqueda por similitud:")
for i, doc in enumerate(resultados, start=1):
    print(f"contenido: {doc.page_content}")
    print(f"metadatos: {doc.metadata}")