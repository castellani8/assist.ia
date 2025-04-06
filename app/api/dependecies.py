from langchain_chroma import Chroma
from groq import Groq
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
import os

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH")

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_function
    )

def get_db():
    return db  # Retorna a instância única do ChromaDB
