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

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
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

def main():
    # Create CLI.
    #parser = argparse.ArgumentParser()
    #parser.add_argument("query_text",type=str,help="The query text.")
    #args = parser.parse_args()
    #query_text = args.query_text
    query_text = input("Enter your query: ")

    # Prepare the DB
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # Search the DB
    results = db._similarity_search_with_relevance_scores(query_text, k=5)
    #print(f"Results length {len(results)}: {results[:1]}")
    count = 0
    for result in results:
        count += 1
        print(f"Result {count} : distance: {result[1]}")
    if len(results) == 0 or results[0][1] < 0:
        print("Unable to find matching results.")
        return
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    #print(prompt)

    #model = ChatOpenAI()
    model = ChatOllama(
        model= "llama3", #"gemma3:12b", #"llama3",  # Or any other pulled model
        temperature=0.8,
        num_predict=256,
    )
    #response_text = model.predict(prompt)
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source",None) for doc, _score in results]
    print()
    formatted_response = f"Response: {response_text.content}\n\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()