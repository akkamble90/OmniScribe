import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Points to the data folder in your D: drive project
CHROMA_PATH = os.path.join("data", "chroma_db")

# Initialize the embedding model (This will download on first run)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store():
    """Helper to initialize or load the Chroma database."""
    return Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings
    )

def add_documents_to_db(chunks, clear_old=True):
    import os
    from langchain_chroma import Chroma
    
    # If we want a fresh start, we don't delete the folder. 
    # We initialize the DB and then empty it.
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings
    )
    
    if clear_old:
        try:
            # Get all IDs and delete them (This clears the data without deleting the folder)
            existing_ids = db.get()['ids']
            if existing_ids:
                db.delete(ids=existing_ids)
                print("Existing vectors cleared from database.")
        except Exception as e:
            print(f"Note: Could not clear existing DB: {e}")

    # Add the new chunks
    db.add_documents(chunks)
    print(f"Successfully added {len(chunks)} new chunks.")

def query_db(query: str, k: int = 3):
    """Searches the database for the most relevant snippets."""
    db = get_vector_store()
    results = db.similarity_search(query, k=k)
    return results