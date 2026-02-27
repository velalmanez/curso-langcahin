from typing import TypedDict, Optional, List, Annotated, Dict, Any
from operator import add
from langchain_google_genai import ChatGoogleGenerativeAI
from rag_system import VectorRAGSystem
from config import *
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

class HelpdeskState(TypedDict):
    consulta: str
    categoria: str
    respuesta_rag: Optional[str]
    confianza: Optional[float]
    fuentes: List[str]
    contexto_rag: Optional[str]
    requiere_humano: bool
    respuesta_humano: Optional[str]
    respuesta_final: Optional[str]
    historial: Annotated[List[str], add]


class HelpdeskGraph:
    """Grafo del sistema de helpdesk."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.1)
        self.rag = VectorRAGSystem(chroma_path=CHROMADB_PATH)
        self.graph = None

    def procesar_rag(self, state):
        """Busca el contexto de la consulta en el sistema RAG."""
        consulta = state["consulta"]
        resultado = self.rag.buscar(consulta)
        return {
            "respuesta_rag": resultado["respuesta"],
            "confianza": resultado["confianza"],
            "fuentes": resultado["fuentes"],
            "contexto_rag": resultado["respuesta"],
            "historial": [
                f"RAG ejecutado con MultiQuertRetriever",
                f"Confianza: {resultado['confianza']:.2f}",
                f"Fuentes consultadas: {len(resultado['fuentes'])}"
            ]
        }
    
    def clasificar_con_contexto(self, state):
       """Clasifica la consulta para responder o escalar, usando el contexto del RAG."""
       consulta = state["consulta"]
       contexto_rag = state.get("contexto_rag", "")
       confianza = state.get("confianza", 0)


       prompt = ChatPromptTemplate.from_template(
           """"
           Analiza esta consulta de helpdesk y decide si puede responderse automáticamente o necesita escalado:

            CONSULTA DEL USUARIO: {consulta}

            INFORMACIÓN ENCONTRADA EN LA BASE DE CONOCIMIENTO:
            {contexto_rag}

            CONFIANZA DE LA BÚSQUEDA: {confianza}

            Criterios de decisión:
            - AUTOMATICO: Si la información de la BD responde completamente la consulta, 
            tiene buena confianza (>0.6), y es un tema estándar/procedimiento conocido
            
            - ESCALADO: Si la información es insuficiente, confianza baja, problema complejo/único,
            requiere acceso a sistemas internos, o involucra decisiones de negocio

            Responde solo con "automatico" o "escalado" y una breve justificación (máximo 20 palabras):"""
        )
       try:
            response = self.llm.invoke(prompt.format(
                consulta=consulta, 
                contexto_rag=contexto_rag, 
                confianza=confianza
            ))

            content = response.content.strip().lower()

            if "automatico" in content or "automático" in content:
                categoria = "automatico"
            elif "escalado" in content:
                categoria = "escalado"
            else:
                categoria = "automatico" if confianza > 0.6 else "escalado"

            return{
                "categoria": categoria,
                "historial": [
                    f"Clasificación realizada por LLM con contexto: {categoria}",
                    f"Justificación: {content}"
                ]
            }
       except Exception as e:
           categoria = "automatico" if confianza > 0.6 else "escalado"
           return{
                "categoria": categoria,
                "historial": [
                     f"Error en clasificación con LLM, se asigna categoría por confianza: {categoria}",
                     f"Error: {str(e)}"
                ]
           }
       
    def preparar_escalado(self, state):
        """Prepara el escaldo a humano"""

        return{
            "requiere_humano": True,
            "historial": [
                "Consulta escalada a humano por clasificación - esperando intervención"
            ]
        }

    def procesar_respuesta_humana(self, state):
        """Procesa la respuesta del humano y a integra en la respuesta final."""
        respuesta_humano = state.get("respuesta_humano", "Respuesta humana no proporcionada")

        if respuesta_humano:

            return{
                "respuesta_final": respuesta_humano,
                "historial": [
                    "Respuesta humana recibida y asignada como respuesta final"
                ]
            }
        
        return{
            "historial": [
                "Esperando respuesta del agente humano"
            ]
        }

    def generar_respuesta_final(self, state):
        """Genera la respuesta final del sistema al ticket del usuario"""
        if state.get("respuesta_final"):
            return{
                "historial": [
                    "Respuesta final ya determinada por humano, no se genera respuesta automática"
                ]
            }

        # si no hay respuesta humana, intentamos generar una respuesta automática con el contexto del RAG
        respuesta_rag = state.get("respuesta_rag", "")
        fuentes = state.get("fuentes", [])

        respuesta_final = respuesta_rag
        if fuentes:
            fuentes_texto = ",".join(fuentes)
            respuesta_final += "\n\nFuentes consultadas:\n" + fuentes_texto

        return{
            "respuesta_final": respuesta_final,
            "historial": [
                "Respuesta final generada a partir del contexto del RAG"
            ]
        }
    
    # funciones de enrutamiento 
    def decidir_desde_clasificacion(self, state):
        """Decide hacia donde ir despues de la calsificación con contexto RAG"""

        categoria = state.get("categoria", "escaldo")

        if categoria == "automatico":
            return "generar_respuesta_final"
        else:
            return "escalado"
        
    def decidir_desde_humano(self, state):
        """Decide si continua o esperar respuesta del humano"""

        respuesta_humano = state.get("respuesta_humano", "")

        if respuesta_humano:
            return "procesar_respuesta_humana"
        else:
            return "esperar"
        
    def crear_grafo(self):
        """Crea el grafo del sistema de helpdesk."""
        graph = StateGraph(HelpdeskGraph)

        # Agregar Nodos
        graph.add_node("rag", self.procesar_rag)
        graph.add_node("clasificar", self.clasificar_con_contexto)
        graph.add_node("escalado", self.preparar_escalado)
        graph.add_node("respuesta_final", self.generar_respuesta_final)
        graph.add_node("procesar_humano", self.procesar_respuesta_humana)

        # Definir la estructura del grafo
        graph.add_edge(START, "rag")
        graph.add_edge("rag", "clasificar")

        # Edges condicionales 
        graph.add_conditional_edges(
            "clasificar", # nodo de origen
            self.decidir_desde_clasificacion, # función de decisión
            {
                "respuesta_final": "respuesta_final",
                "escalado": "escalado"
            }
        )
        graph.add_conditional_edges(
            "escalado",
            self.decidir_desde_humano,
            {
                "procesar_humano": "procesar_humano",
                "esperar": END # pausar ejecucion del grafo hasta que responda el humano
            }
        )

        graph.add_edge("procesar_humano", END)
        graph.add_edge("respuesta_final", END)

        self.graph = graph

        return graph
    
    def compilar(self):
        """Compila el grafo para su ejecución."""

        if not self.graph:
            self.crear_grafo()

        conn = sqlite3.connect("helpdesk.db", check_same_thread=False)

        checkpointer = SqliteSaver(conn)

        compiled = self.graph.compile(
            checkpointer=checkpointer,
            interrupt_before=["procesar_humano"]    
        )

        return compiled

def crear_helpdesk():
    helpdesk = HelpdeskGraph()
    return helpdesk.compilar()