from langchain_google_genai import ChatGoogleGenerativeAI
from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts

def crear_evaluador_cv():
    modelo_base = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash", 
        temperature=0.2
    )

    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    cadena_evaluacion = chat_prompt | modelo_estructurado

    return cadena_evaluacion

def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try: 
        cadena_evaluacion = crear_evaluador_cv()
        resultado = cadena_evaluacion.invoke({
            "texto_cv": texto_cv,
            "descripcion_puesto": descripcion_puesto
        })

        return resultado
    
    except Exception as e:
        return AnalisisCV(
            nombre_candidato="Error en procesamiento",
            experiencia_años=0,
            habilidades_clave=["Error al procesar cv."],
            educacion="no se puede detemrinar. ",
            experiencia_relevante= "Error durante el analisis. ",
            fortalezas=["Requiere revision manual de CV."],
            areas_mejora=["verificar formato y legibilidad del PDF"],
            porcentaje_ajuste=0
        )
