from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.retrievers.multi_query import MultiQueryRetriever


vector_store = Chroma.from_documents(
    embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
    persist_directory="G:\\TRABAJO\\CURSOS\\curso-langcahin\\curso_langchain\\tema_3\\vector_store_contratos"
)

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.7)

base_retriever = vector_store.as_retriever(search_type="similarity", serach_kwargs={"k":3})
retriever = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm) #Reformula la query utilizando IA para hacer la consulta varias veces

consulta = "¿Cuáles son las obligaciones principales del arrendatario según el contrato de arrendamiento?"

#Hacer busqueda por similitud
resultados = retriever.invoke(consulta)

print("Resultados de la búsqueda por similitud:")
for i, doc in enumerate(resultados, start=1):
    print(f"contenido: {doc.page_content}")
    print(f"metadatos: {doc.metadata}")