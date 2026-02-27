from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

#guarda el historial en RAM
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.7)

prompt= ChatPromptTemplate.from_messages([
    ("system","Eres un asistente util"),

    #Agregamos el historial de mensajes al chatpromptTemplate
    MessagesPlaceholder(variable_name="history"),
    
    ("human", "{input}")
])

chain = prompt | llm

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# cadena con memoria automatica por sesion
chain_whith_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
) 


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

    response = chain_whith_memory.invoke(
        {"input": user_input},
        #establece la sesion
        config={"configurable": {"session_id": session_id}}

    )
    print("Asistente: ", response.content)