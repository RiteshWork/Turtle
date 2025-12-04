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

class LLM_Model:
    def __init__(self, model_name="llama3"):
        self.model = model_name
        self.temperature = 0.8
        self.num_predict = 256
    
    def model_init(self):
        model = ChatOllama(
            model = self.model,
            temperature = self.temperature,
            num_predicts = self.num_predict
        )

        return model
    
    
