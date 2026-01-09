from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

plantilla_sistema = SystemMessagePromptTemplate.from_template(
    "Eres un {rol} especializado en {especialidad}. Responde de manera {tono}"
)

plantilla_humano = HumanMessagePromptTemplate.from_template(
    "Mi pregunta sobre {tema} es: {pregunta}"
)

# composicion de ambas plantillas
chat_prompt = ChatPromptTemplate.from_messages([ 
    plantilla_sistema,
    plantilla_humano
])

# implementacion de varibles de las plantillas
mensajes = chat_prompt.format_messages(
    rol = "entrenador de fuerza",
    especialidad = "entrenamientos para powerlifting",
    tono = "profesional pero accesible",
    tema = "programacion de entrenamiento",
    pregunta = "en que consiste la periodizacion ondulante?"
)

for m in mensajes:
    print(m.content)