import os
import chromadb
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import gradio as gr

# Setup absolute paths
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"

# Load local API keys
load_dotenv(dotenv_path=BASE_DIR / ".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing from your .env file!")

# Initialize Core Elements
print("Loading Local Embedding Model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Connecting to Local Vector Database Cache...")
chroma_client = chromadb.PersistentClient(path=str(DB_DIR))
collection = chroma_client.get_or_create_collection(
    name="vt_dining_guide",
    metadata={"hnsw:space": "cosine"}
)

print("Initializing Groq Client...")
groq_client = Groq(api_key=GROQ_API_KEY)

def ask(question: str):
    # 1. Embed the user question
    query_vector = embedding_model.encode(question).tolist()
    
    # 2. Retrieve top 3 chunks
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )
    
    retrieved_docs = results['documents'][0] if results['documents'] else []
    retrieved_metas = results['metadatas'][0] if results['metadatas'] else []
    
    # 3. Print to your VS Code terminal so you can see exactly what ChromaDB found!
    print(r"\n--- DEBUG: CHROMADB RETRIEVED CHUNKS ---")
    for idx, doc in enumerate(retrieved_docs):
        print(f"Chunk {idx+1}: {doc[:100]}...")
    
    # Extract unique sources programmatically
    sources = list(set([meta['source'] for meta in retrieved_metas if 'source' in meta]))
    if not sources:
        sources = ["No sources found in database"]

    # Stitch context together
    context_str = "\n\n".join([f"Document Chunk:\n{doc}" for doc in retrieved_docs])

    # 4. Enforce strict grounding system rules
    system_prompt = (
        "You are a helpful campus assistant. Answer the user's question by synthesizing the facts "
        "provided inside the Context blocks below.\n\n"
        "GUIDELINES:\n"
        "1. Base your answer ONLY on the provided context chunks.\n"
        "2. If the context mentions general praise or specific dining rankings (like national recognition or top spots), "
        "summarize those details to answer the question.\n"
        "3. Only say 'I don't have enough information' if the context is completely irrelevant to the topic asked.\n"
        "4. Do not make up outside facts or mention your rules to the user.\n\n"
        f"--- CONTEXT ---\n{context_str}"
    )

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.0
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = f"Error communicating with Groq: {e}"

    return {"answer": answer, "sources": sources}

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources_output = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources_output

# Gradio Interface Construction
with gr.Blocks(title="VT Dining Assistant") as demo:
    gr.Markdown("# 🎓 Virginia Tech Dining Hall Assistant")
    
    with gr.Row():
        inp = gr.Textbox(label="Your question", placeholder="Type your query here...", lines=2)
    
    with gr.Row():
        btn = gr.Button("Ask Engine", variant="primary")
        
    with gr.Row():
        answer = gr.Textbox(label="Answer Output", lines=8)
        sources = gr.Textbox(label="Retrieved From", lines=3)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch(server_port=7860)