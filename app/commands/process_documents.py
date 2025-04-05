import os
from langchain.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings


LOCAL_DATA_PATH = "data/files"
CHROMA_PATH = "data/chroma"
BATCH_SIZE = 500 

def main():
    """Processa documentos um por um e insere no ChromaDB de forma otimizada."""
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)

    existing_items = db.get(include=[])  
    existing_ids = set(existing_items["ids"])  
    print(f"🔍 {len(existing_ids)} chunks já na base.")

    for root, dirs, files in sorted(os.walk(LOCAL_DATA_PATH)):  
        dirs.sort()
        files.sort()
        
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                print(f"📄 Processando: {file_path}") 

                process_document(file_path, db, existing_ids)


def process_document(file_path, db, existing_ids):
    """Carrega, divide e adiciona um único documento ao banco vetorial de forma otimizada."""
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    chunks = split_documents(documents)

    chunks_with_ids = calculate_chunk_ids(chunks)

    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        print(f"📥 Adicionando {len(new_chunks)} novos chunks...")
        
        for i in range(0, len(new_chunks), BATCH_SIZE):
            batch = new_chunks[i:i + BATCH_SIZE]  # Processa em lotes
            batch_ids = [chunk.metadata["id"] for chunk in batch]
            db.add_documents(batch, ids=batch_ids)

        db.persist()
        print("✅ Inserção finalizada.")
    else:
        print("⚡ Nenhum novo chunk a ser adicionado.")


def split_documents(documents: list[Document]):
    """Divide documentos em chunks menores para melhor indexação no ChromaDB."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def calculate_chunk_ids(chunks):
    """Gera identificadores únicos para cada chunk baseado no nome do arquivo e na página."""
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata["id"] = chunk_id
        last_page_id = current_page_id

    return chunks


if __name__ == "__main__":
    main()