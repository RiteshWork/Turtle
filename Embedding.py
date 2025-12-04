import argparse
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
import os
import shutil
from dotenv import load_dotenv

class Embedding:
    def __init__(self, model_name="nomic-ai/modernbert-embed-base"):
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)
    
    def embedding_init(self):
        embedding = HuggingFaceEmbeddings(
            model_name = self.model_name,
            model_kwargs = {'device':'cpu'},
            encode_kwargs = {'normalize_embeddings':False}
        )

        return embedding
