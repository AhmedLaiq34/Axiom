import os
import shutil
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from config import embeddings, CHROMA_PATH, DATA_PATH, POPPLER_BIN

def build_vector_db(course_code="PF-Spring2025", root_directory=DATA_PATH):
    all_docs = []
    
    if not os.path.exists(root_directory):
        os.makedirs(root_directory)
        print(f"📁 Created '{root_directory}'. Add your files and re-run.")
        return None

    for root, dirs, files in os.walk(root_directory):
        source_type = os.path.basename(root) if root != root_directory else "General"
        
        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.join(root, filename)
                print(f"\n🚀 VISION START: Processing [{source_type}] -> {filename}")
                
                loader = UnstructuredLoader(
                    file_path,
                    strategy="hi_res",          # Triggers Poppler + Tesseract
                    model_name="chipper",       # Vision layout analyzer
                    partition_via_api=False,    
                    extract_image_block_types=["Image", "Table"], 
                    poppler_path=POPPLER_BIN     
                )
                
                pages = loader.load()
                
                # --- LIVE DEBUG PRINT ---
                print(f"📑 Extracted {len(pages)} elements from PDF.")
                for i, page in enumerate(pages[:3]): # Show first 3 elements for brevity
                    print(f"\n--- [PREVIEW] Element {i+1} from {filename} ---")
                    print(f"Context: {page.page_content[:300]}...") # First 300 chars
                    print(f"Metadata: {page.metadata.get('category')} | Page: {page.metadata.get('page_number')}")
                    print("-" * 40)

                all_docs.extend(pages)

    # 2026 Semantic Chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_docs)

    print(f"\n📦 FINAL STAGE: Created {len(chunks)} searchable chunks.")
    
    # Optional: Print a random chunk to see the final form
    if chunks:
        print("\n--- [FINAL CHROME-READY CHUNK] ---")
        print(chunks[0].page_content)
        print(f"Metadata: {chunks[0].metadata}")
        print("----------------------------------\n")

    # Wipe and Save
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"✅ Database Persisted to {CHROMA_PATH}")
    return vector_db

if __name__ == "__main__":
    build_vector_db()