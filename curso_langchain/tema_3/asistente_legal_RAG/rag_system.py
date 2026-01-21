from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_classic.retrievers import EnsembleRetriever
import streamlit as st

from config import * # uso de veriables globales 
from prompts import *

def intialize_rag_system():
    # vector Store
    vector_store=Chroma(
        embedding_function=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=VECTOR_STORE_CONTRATOS
    )

    # Modelos
    llm_queries = ChatGoogleGenerativeAI(model=QUERY_MODEL, temperature=0)
    llm_generation = ChatGoogleGenerativeAI(model=GENERATION_MODEL, temperature=0.5)

    # retriever Base
    base_retriever = vector_store.as_retriever(
        search_type = SEARCH_TYPE,
        search_kwargs={
            "k": SEARCH_K,
            "lambda_mult": MMR_DIVERSITY_LAMBDA,
            "fetch_k": MMR_FETCH_K
        }
    )

    # retriver adicion con similitud por coseno
    similarity_retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k": SEARCH_K}
    )

    # prompt personalizado para multiQueryRetriever
    multi_query_prompt = PromptTemplate.from_template(MULTI_QUERY_PROMPT)

    # MultiQueryretriever con prompt personalizado
    mmr_multi_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm_queries,
        prompt=multi_query_prompt
    )

    # Ensemble retriever que combina MMR con similarity
    if ENABLE_HYBRID_SEARCH:
        ensemble_retriever = EnsembleRetriever(
            retrievers=[mmr_multi_retriever, similarity_retriever],
            weights=[0.7, 0.3], # mayor peso a MMR
            similarity_threshold = SIMILARITY_THRESHOLD
        )
        final_retriever = ensemble_retriever
    else:
        final_retriever = mmr_multi_retriever

    prompt = PromptTemplate.from_template(RAG_TEMPLATE)

    # preprocesamiento de documentos
    def format_docs(docs):
        formatted = []

        for i, doc in enumerate(docs, 1):
            header = f"[Fragmento {i}]"
            
            if doc.metadata: 
                if 'source' in doc.metadata: 
                    source = doc.metadata['source'].split("\\")[-1] if '\\' in doc.metadata['source'] else doc.metadata['source']
                    header += f" - Fuente : {source}"
                if 'page' in doc.metadata:
                    header += f" - Pagina: {doc.metadata['page']}"
            
            content = doc.page_content.strip()
            formatted.append(f"{header} \n {content}")
        
        return "\n\n".join(formatted)


    rag_cahin = (
        {
            "context": final_retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt 
        | llm_generation 
        | StrOutputParser()
    )

    return rag_cahin, mmr_multi_retriever

def query_rag(question): 
    try:
        rag_chain, retriever= intialize_rag_system()

        #Obtener respuesta
        response = rag_chain.invoke(question)

        # Obtener documentos para mostrarlos
        docs = retriever.invoke(question)

        # Formatear los documentos para mostrar
        docs_info = []

        for i,doc in enumerate(docs, 1):
            doc_info = {
                "fragmento": i,
                "contenido": doc.page_content,
                "fuente": doc.metadata.get('source', 'No especificado').split("\\")[-1],
                "pagina": doc.metadata.get('page', 'No especificada')
            }
            docs_info.append(doc_info)
        
        return response, docs_info
    except Exception as e:
        error_msg = f"Error al procesar la consulta: {str(e)}"
        return error_msg, []
    
def get_retriever_info(): 
    """Obtiene la informacion sobre la configuracion del retriever"""

    return{
        "tipo":f"{SEARCH_TYPE.upper()} + MultiQuery" + (" + Hybrid" if ENABLE_HYBRID_SEARCH else ""),
        "documentos": SEARCH_K,
        "diversidad": MMR_DIVERSITY_LAMBDA,
        "candidatos": MMR_FETCH_K,
        "umbral": SIMILARITY_THRESHOLD if ENABLE_HYBRID_SEARCH else ""
    }