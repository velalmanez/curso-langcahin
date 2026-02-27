from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.7)

prompt= ChatPromptTemplate.from_messages([
    ("system","Eres un asistente util"),

    #Agregamos el historial de mensajes al chatpromptTemplate
    MessagesPlaceholder(variable_name="history"),
    
    ("human", "{input}")
])

chain = prompt | llm

history=[]

print("Chat en terminal (ecribe 'salir' para terminar)\n")

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

    response = chain.invoke({"history":history, "input": user_input})
    print("Asistente: ", response.content)

    #Actualizamos el historial de mensajes
    history.extend([
        HumanMessage(content=user_input),
        AIMessage(content=response.content)
    ])