# Configuracion de modelos
EMBEDDING_MODEL = "gemini-embedding-001"
QUERY_MODEL = "gemini-2.5-flash-lite" # modelo para generacion de prompts
GENERATION_MODEL = "gemini-2.5-flash" # modelo para generacion de resultados

# Configuracion de vector store
VECTOR_STORE_CONTRATOS = "G:\\TRABAJO\\CURSOS\\curso-langcahin\\curso_langchain\\tema_3\\vector_store_contratos"

# Configuracion del retriever
SEARCH_TYPE = "mmr"
MMR_DIVERSITY_LAMBDA = 0.7 # parametro para diversidad de documentos
MMR_FETCH_K = 20 # cantidad de documentos relevantes a evaluar
SEARCH_K = 2 #numero de documentos finales que devuelve

# confuiguracion alternativa para retriever hibrido
ENABLE_HYBRID_SEARCH = True
SIMILARITY_THRESHOLD = 0.75