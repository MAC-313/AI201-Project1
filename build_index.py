import os
import json
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

def main():
    print("=== Stage 1: Initializing Local Embedding Model ===")
    # Load the local model specified in your planning.md (no API key required)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    print("\n=== Stage 2: Connecting to Local Vector Store ===")
    # Set up ChromaDB to persist data locally inside your project folder
    db_path = "chroma_db"
    client = chromadb.PersistentClient(path=db_path)
    
    # Create or fetch your specific collection
    collection = client.get_or_create_collection("vt_dining_guide")
    
    print("\n=== Stage 3: Loading and Processing Generated Chunks ===")
    chunks_file = Path("data/chunks.json")
    if not chunks_file.exists():
        print("ERROR: data/chunks.json not found! Run ingest.py first to generate chunks.")
        return
        
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    print(f"Loaded {len(chunks)} chunks from disk.")
    
    # Prepare lists for ChromaDB ingestion
    documents = []
    embeddings = []
    ids = []
    metadatas = []
    
    print("Generating embeddings (this may take a moment running locally)...")
    for idx, item in enumerate(chunks):
        text_content = item["text"]
        source_name = item["source"]
        chunk_id = item["chunk_id"]
        
        # Calculate local embedding vector
        vector = model.encode(text_content).tolist()
        
        documents.append(text_content)
        embeddings.append(vector)
        # Create a completely unique string ID for this chunk
        ids.append(f"{source_name}_chunk_{chunk_id}")
        metadatas.append({
            "source": source_name,
            "chunk_id": chunk_id
        })
        
    print("\n=== Stage 4: Writing Vectors to ChromaDB ===")
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Successfully indexed and saved {len(documents)} chunks to '{db_path}/'.")
    
    print("\n=== Stage 5: Running Retrieval Diagnostic Check (Milestone 4) ===")
    # Define 3 test queries directly from your evaluation plan spec
    test_queries = [
        "Which dining hall receives the most praise for food quality?",
        "Which location is criticized for long wait times?",
        "Which location is best for late-night dining?"
    ]
    
    for q_idx, query in enumerate(test_queries, 1):
        print(f"\n--- Test Query {q_idx}: '{query}' ---")
        
        # Embed the incoming user test query
        query_vector = model.encode(query).tolist()
        
        # Request top-k=4 nearest chunks
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=4
        )
        
        # Unpack and inspect returned data
        retrieved_docs = results["documents"][0]
        retrieved_meta = results["metadatas"][0]
        retrieved_dist = results["distances"][0] if "distances" in results and results["distances"] else [0.0]*4
        
        for i in range(len(retrieved_docs)):
            print(f"  [{i+1}] Source: {retrieved_meta[i]['source']} (Chunk #{retrieved_meta[i]['chunk_id']})")
            print(f"      Distance Score: {retrieved_dist[i]:.4f}")
            # Snippet of retrieved text for terminal readability
            snippet = retrieved_docs[i][:140].replace('\n', ' ') + "..."
            print(f"      Text: {snippet}\n")

if __name__ == "__main__":
    main()