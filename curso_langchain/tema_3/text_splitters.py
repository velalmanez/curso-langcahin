from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. cargar el documento PDF
loader = PyPDFLoader("G:\\TRABAJO\\CURSOS\\curso-langcahin\\curso_langchain\\tema_3\\quijote.pdf")
pages = loader.load()

# dividir el texto en fragmentos mas pequeños
text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=3000, # cantidad de caracteres por fragmento
    chunk_overlap=200, # caracteres de solapamiento entre fragmentos
)

# dividir el documento en fragmentos (chunks)
chunks = text_spliter.split_documents(pages)

# 2. combinar todas las páginas en un solo string
full_text  = ""
for page in pages:
    full_text += page.page_content + "\n"

# 3. pasar el texto completo al modelo de lenguaje
llm = ChatGoogleGenerativeAI(model_name="gemini-2.5-flash", temperature=0.2)
sumaries = []

i = 0
for chunk in chunks:
    if i > 10:
        break 
    response = llm.invoke("Haz un resumen de los puntos mas importantes del siguiente texto:\n" + chunk.page_content)
    sumaries.append(response)
    i += 1


# 4. combinar los resúmenes en un solo texto
final_summary = llm.invoke(f"Combina los siguientes resúmenes en un solo resumen coherente: {' '.join(sumaries)}")
print(final_summary.content)