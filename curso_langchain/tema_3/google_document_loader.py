from langchain_community.document_loaders import GoogleDriveLoader
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
token_path = os.getenv("GOOGLE_TOKEN_PATH")

loader =  GoogleDriveLoader(
    folder_id="1SXZJlLLxvl8i9W0zEl_rTBZGJgPGcvQy",
    credentials_path=credentials_path,
    token_path=token_path,
    recursive=True
)

documents = loader.load()

print(f"Metadatos: {documents[0].metadata}")
print(f"Contenido: {documents[0].page_content}")