from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor de español a ingles muy preciso."),
    ("human", "{texto}")
])

mensajes = chat_prompt.format_messages(texto="Hola mundio, ¿Como estas?")

for m in mensajes:
    print(f"{type(m)}: {m.content}")