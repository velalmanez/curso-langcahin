from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import streamlit as st

# configurar la pagina de la aplicacion
st.set_page_config(page_title="Chat GPT offline", page_icon="🤖")
st.title("Chat yipiti offline")
st.markdown("Este es un chatbot de prueba utilizando Langchain + Streamlit")

with st.sidebar:
    st.header("CONFIGURACIÓN")
    temperature = st.slider("Temperatura del modelo", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    model_name = st.selectbox("Selecciona el modelo", options=["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"])

    personalidad = st.selectbox(
        "Personalidad del asistente",
        [
            "Útil y amigable",
            "Profesional y formal",
            "Casual y relajado",
            "Experto técnico",
            "Creativo y divertido"
        ]
    )

    # inicializar el modelo de lenguaje
    chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

    # mensajes del sistema segun la persoanlidad 
    system_messages ={
        "Útil y amigable" : "Eres un asistente util y amigables llamado ChatBot Pro. Responde de manera clara y concisa.",
        "Profesional y formal": "Eres un asistente profesional y fromal. Proporciona respuestas precisas y bien estructuradas.",
        "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
        "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
        "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
    }

    # Chat Prompt template con personalidad dinamica  
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidad]),
        ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
    ])

    # Crear cadena LCEL
    cadena = chat_prompt | chat_model   

# inicializar el historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []


# mostrar mensajes previos
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
            historial_texto += f"Usuario: {msg.content}\n"
    elif isinstance(msg, AIMessage):
            historial_texto += f"Asistente: {msg.content}\n"

    # Botón para limpiar la conversación
    if st.button("Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()

# Cuadro de entrada de usuario
pregunta = st.chat_input("Escribe tu mensaje aquí...")

if pregunta:
    # Mostrar el mensaje del usuario en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)

    try: 
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # Sreaming de la respuesta del modelo
            for chunk in cadena.stream(
                {
                    "mensaje": pregunta,
                    "historial": st.session_state.messages,
                }
            ):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")  # Indicador de escritura

            response_placeholder.markdown(full_response)  # Respuesta final sin indicador

    except Exception as e:
        st.error(f"Se produjo un error al generar la respuesta: {e}")
        st.info("Por favor, verifica tu configuración y vuelve a intentarlo.")