from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from app.services.external.groq import get_groq_response
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH")

PROMPT_TEMPLATE = """
***INSTRUCTIONS***
{instructions}

***TECHNICAL CONTEXT***
{technical_context}
"""

def query(instructions: str, query: str):
    technical_context, sources = get_relevant_docs_from_chroma(query)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    sys_msg = prompt_template.format(
        instructions=instructions,
        technical_context=technical_context
    )

    response = get_groq_response(sys_msg, query)
    
    return response

def get_relevant_docs_from_chroma(query_text):
    if not os.path.exists(CHROMA_PATH):
        return "", []
    
    try:
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)

        results = db.similarity_search_with_score(query_text, k=20)
        relevant_docs = [(doc, score) for doc, score in results if score <= 40]

        if not relevant_docs:
            technical_context = "Não foram encontrados chunks."
        else:
             technical_context = "\n\n---\n\n".join([doc.page_content for doc, _ in relevant_docs])

        sources = [{
                "score": score,
                "source": doc.metadata.get("source", "Fonte desconhecida"),
                "source_id": doc.metadata.get("id", "sem_id"),
                "excerpt": doc.page_content[:200]
            } for doc, score in results]
        
        return technical_context, sources
    except Exception as e:
        return "", []