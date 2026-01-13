import PyPDF2
from io import BytesIO

def extraer_texto_pdf(archivio_pdf):
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivio_pdf.read()))
        texto_completo = ""

        #Itera sobre cada pagina del pdf
        for numero_pagina, pagina in enumerate(pdf_reader.pages, 1):
            texto_pagina = pagina.extract_text()

            #Concatena el texto relevante por cada pagina
            if texto_pagina.strip():
                texto_completo += f"\n-- PAGINA {numero_pagina} ---\n"
                texto_completo += texto_pagina + "\n"

        texto_completo = texto_completo.strip()

        if not texto_completo:
            return "Error: El PDF parece estar vacio o contener solo imagenes."
        return texto_completo
    except Exception as e:
        return f"Error al procesar el archivo PDF: {str(e)}"