import PyPDF2
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

import os

pdf_file = "./documents"
web_links = ["https://www.casablancacity.ma/ar/demarche/41/autorisation-de-dresser-lacte-de-mariage",
             "https://www.passeport.ma/",
            "https://www.demarchesmaroc.com"]# Update URLs as necessary

def read_pdf(file_path):
    try:
        with open(file_path, "rb") as file:
            pdfReader = PyPDF2.PdfReader(file)
            all_page_text = ""
            for page in pdfReader.pages:
                all_page_text += page.extract_text() + "\n"
        return all_page_text
    except Exception as e:
        print(f"Failed to read PDF file at {file_path}: {e}")
        return ""

def load_documents_from_directory(directory_path):
    directory_path = pdf_file
    files = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith(".pdf")]
    documents = [Document(page_content=read_pdf(file)) for file in files]
    return documents

def load_web_documents(urls):
    documents = []
    for url in urls:
        loader = WebBaseLoader(url)
        web_content = loader.load()
        documents.extend([Document(page_content=item.page_content) for item in web_content])
    return documents



def load_all_documents():
    pdf_documents = load_documents_from_directory(pdf_file)
    web_documents = load_web_documents(web_links)
    return pdf_documents + web_documents

# Use this function to process all documents
all_documents = load_all_documents()
texts = [doc.page_content for doc in all_documents]

def ingest_into_vector_store(combined_texts):
    # Process combined documents
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size= 3400, chunk_overlap=20, separator=".")
    doc_splits = text_splitter.split_documents([Document(page_content=text) for text in combined_texts])
    
    # Initialize the Chroma vector store with a specific collection name
    db = Chroma(persist_directory="./chroma_db", embedding_function=OllamaEmbeddings(model="mxbai-embed-large:latest"), collection_name="rag-chroma")

    # Add documents to Chroma and persist the data
    db.add_documents(doc_splits)  # Ensure documents is a list of dicts with 'page_content'
    db.persist()

    print("Data has been ingested into vector database.")


if __name__ == "__main__":
    all_documents = load_all_documents()
    if all_documents:
        combined_texts = [doc.page_content for doc in all_documents]
        ingest_into_vector_store(combined_texts)
    else:
        print("No data to process.")

