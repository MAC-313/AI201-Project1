import os
import json
import re
from pathlib import Path

DATA_DIR = Path(r"C:\Users\Muhammad Chawla\Desktop\Codepath assignments\Project 1\AI201-Project1\data")
OUTPUT_FILE = DATA_DIR / "chunks.json"

# Semantic Window Tuning Parameters
MAX_CHUNK_SENTENCES = 4
OVERLAP_SENTENCES = 1

def deep_clean_text(text):
    """Forcefully repairs uneven source layout configurations."""
    # 1. Neutralize carriage returns and replace broken newlines with spaces
    text = text.replace("\r\n", " ").replace("\n", " ").replace("\t", " ")
    
    # 2. Repair common text extraction spacing failures
    text = re.sub(r'\s+([.,!?])', r'\1', text) 
    
    # 3. Collapse multiple whitespaces into clean single gaps
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()

def chunk_by_sentence_boundaries(text, max_sentences=4, overlap_sentences=1):
    """Slices documents by whole sentences only after normalization cleanup."""
    # Split text strictly on real punctuation boundaries followed by a space
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 3] # Filter out noise
    
    chunks = []
    i = 0
    while i < len(sentences):
        window = sentences[i : i + max_sentences]
        if not window:
            break
            
        chunk_text = " ".join(window)
        if len(chunk_text.strip()) > 10:  # Drop useless string fragments
            chunks.append(chunk_text.strip())
            
        i += (max_sentences - overlap_sentences)
        
    return chunks

def main():
    print("=== Running Normalized Pipeline Framework ===")
    all_chunks = []
    
    txt_files = list(DATA_DIR.glob("*.txt"))
    if not txt_files:
        print(f"ERROR: No target documents detected inside {DATA_DIR}")
        return

    print(f"Synthesizing {len(txt_files)} source text files...")
    
    for file_path in txt_files:
        if file_path.name == "chunks.json":
            continue
            
        # Read file with error-resistant boundaries
        raw_text = file_path.read_text(encoding="utf-8", errors="ignore")
        
        # Apply normalization sequence
        cleaned_text = deep_clean_text(raw_text)
        
        # Convert text array into safe windows
        chunks = chunk_by_sentence_boundaries(cleaned_text, MAX_CHUNK_SENTENCES, OVERLAP_SENTENCES)
        
        print(f"  -> Synthesized {file_path.name}: Generated {len(chunks)} clean segments.")
        
        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": file_path.name,
                "chunk_id": idx
            })
            
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)
        
    print(f"\nCompleted! Total uniform chunks written to database input manifest: {len(all_chunks)}")

if __name__ == "__main__":
    main()