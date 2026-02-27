from langgraph.graph import MessagesState, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import trim_messages


llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.7)

class WindowedState(MessagesState):
    pass

workflow = StateGraph(state_schema=WindowedState)

trimmer = trim_messages(
    # indica que parte de los mensajes tomar (last = ultimos)
    strategy="last",
    # cantidad de tokens a considerar
    max_tokens=4,
    #funcion para determinar como contar tokens (ultimos 4 mensajes)
    token_counter=len,
    # indica donde comenzar la division (a partir del mensaje enviado por el humano)
    start_on= "human",
    # indica si se incluye el prompt del sistema 
    include_system=True
)

def chatbot_node(state):
    """Nodo que procesa mensajes y genera respuesta"""

    # Recupera el listado de mensajes y si supera los 4 indicados toma los ultimos 4 mensajes 
    trimmed_messages = trimmer.invoke(state["messages"])

    #Define el comportamiento del modelo
    system_prompt = "Eres un asistente amigable que recuerda conversaciones previas"
    
    #Agrega los ultimos 4 mensajes 
    messages = [SystemMessage(content=system_prompt)] + state["messages"] + trimmed_messages

    response = llm.invoke(messages)
    
    #Actualiza el estado 
    return {"messages": [response]}

workflow.add_node("chatbot", chatbot_node)
workflow.add_edge(START, "chatbot")

# Compilar el grafo
memory = MemorySaver()
# cada que se complie, guarda el historial en memoria RAM
app = workflow.compile(checkpointer=memory)

def chat( message, thread_id="sesion_terminal"):

    config={"configurable": {"thread_id":thread_id}}
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config)
    return result["messages"][-1].content

if __name__ == "__main__":
    print("Chat en terminal (ecribe 'salir' para terminar)\n")

    # se genera el session_id
    session_id = "sesion_terminal"

    while True: 
        try: 
            user_input=input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego")
            break

        if not user_input:
            continue
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("\nHasta luego")
            break

        response = chat(user_input, session_id)
        print("Asistente: ", response)