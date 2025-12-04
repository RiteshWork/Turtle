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
from Embedding import Embedding

class VectorDB:
    def __init__(self,data_path='data/'):
        self.DATA_PATH = data_path
        self.CHROMA_PATH = 'chroma'
        self.chunk_size = 400
        self.chunk_overlap = 100
        self.embedding = self.get_embedding_function()

    def load_documents(self):
        loader = DirectoryLoader(self.DATA_PATH, glob='*.md')
        documents = loader.load()
        return documents

    def split_text(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function = len,
            add_start_index = True,
        )

        chunks = text_splitter.split_documents(documents)
        return chunks

    def get_embedding_function(self):
        model_name = "nomic-ai/modernbert-embed-base"
        em = Embedding(model_name)
        embedding = em.embedding_init()
        return embedding


    def save_to_chroma(self,chunks):
        if os.path.exists(self.CHROMA_PATH):
            shutil.rmtree(self.CHROMA_PATH)

        db = Chroma.from_documents(
            chunks, self.embedding, persist_directory=self.CHROMA_PATH
        )
        db.persist()

    def generate_data_store(self):
        documents = self.load_documents()
        chunks = self.split_text(documents)
        self.save_to_chroma(chunks)
    
    def query_text(self,query):
        db = Chroma(persist_directory=self.CHROMA_PATH, embedding_function=self.embedding)
    
        # Search the DB
        results = db._similarity_search_with_relevance_scores(query, k=5)
        return results
    
