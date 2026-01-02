from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
import streamlit as st

# configurar la pagina de la aplicacion
st.set_page_config(page_title="Chat GPT offline", page_icon="🤖")
st.title("Chat yipiti offline")
st.markdown("Este es un chatbot de prueba utilizando Langchain + Streamlit")

with st.sidebar:
    st.header("CONFIGURACIÓN")
    temperature = st.slider("Temperatura del modelo", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    model_name = st.selectbox("Selecciona el modelo", options=["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"])

    # inicializar el modelo de lenguaje
    chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

# inicializar el historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente útil. Responde a la siguiente pregunta de manera clara y concisa
    Historial de conversación: {historial}
    Responde de forma clara y concisa a la siguiente pregunta: {mensaje}"""
)

# Crear cadena LCEL
cadena = prompt_template | chat_model

# mostrar mensajes previos
for msg in st.session_state.messages:
    if isinstance(msg, SystemMessage):
        continue

    role = "assistant" if isinstance(msg, AIMessage) else "user"

    with st.chat_message(role):
        st.markdown(msg.content)

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