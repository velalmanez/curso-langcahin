from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

loader = PyPDFLoader("G:\\TRABAJO\\CURSOS\\curso-langcahin\\curso_langchain\\tema_3\\CV.pdf")

docs = loader.load()

for i, page in enumerate(docs):
    print(f"--- Page {i + 1} ---")
    print(f"Content: {page.page_content}")
    print(f"Metadata: {page.metadata}")

# Example of loading a web page
web_loader = WebBaseLoader("https://example.com")
web_docs = web_loader.load()
print(f"Loaded {len(web_docs)} documents from the web page.")