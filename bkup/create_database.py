from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
import os
import shutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma"
DATA_PATH = "data/"

def get_embedding_function():
    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    #return embeddings
    #model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_name = "nomic-ai/modernbert-embed-base"
    model = SentenceTransformer(model_name)
    embeddings = HuggingFaceEmbeddings(
        model_name = model_name,
        model_kwargs = {'device':'cpu'},
        encode_kwargs={'normalize_embeddings':False}
    )

    return embeddings

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob='*.md')
    documents = loader.load()
    return documents

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)}" )
    document = chunks[10]
    #print(document.page_content)
    #print(document.metadata)

    return chunks

def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, get_embedding_function(), persist_directory=CHROMA_PATH 
    )

    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}")

def main():
    generate_data_store()

if __name__ == "__main__":
    main()

