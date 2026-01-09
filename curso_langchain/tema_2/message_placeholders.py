from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "eres un asistente util que mantiene el contexto de la conversacion"),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "{pregunta_actual}")
])

#Simulacion dde historial de conversacion 
historial_conversacion = [
    HumanMessage(content="Cual es la capital de Francia?"),
    AIMessage(content="La capital de Francia es Paris"),
    HumanMessage(content="Y cuantos habitantes tiene?"),
    AIMessage(content="Paris tiene aproximadamente 2.2 millones de habitantes en la ciudad")
]

mensajes = chat_prompt.format_messages(
    historial = historial_conversacion,
    pregunta = "Puedes decirme algo interesante de su arquitectura"
)


