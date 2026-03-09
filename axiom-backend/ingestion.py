import os
import shutil
import time
# NEW: Import for fixing the metadata error
from langchain_community.vectorstores.utils import filter_complex_metadata 
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from config import embeddings, CHROMA_PATH, DATA_PATH, POPPLER_BIN

def build_vector_db(course_code="PF-Spring2025", root_directory=DATA_PATH):
    all_docs = []
    
    if not os.path.exists(root_directory):
        os.makedirs(root_directory)
        print(f"📁 Created {root_directory}. Add PDFs and re-run.")
        return None

    # --- 1. VISION & OCR PROCESSING ---
    for root, dirs, files in os.walk(root_directory):
        source_type = os.path.basename(root) if root != root_directory else "General"
        
        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.join(root, filename)
                print(f"🧠 High-Res Vision Processing [{source_type}]: {filename}...")
                
                loader = UnstructuredLoader(
                    file_path,
                    strategy="hi_res",
                    partition_via_api=False,
                    extract_image_block_types=["Image", "Table"],
                    extract_image_block_to_payload=True,
                    poppler_path=POPPLER_BIN 
                )
                
                pages = loader.load()
                
                for i, page in enumerate(pages):
                    is_scanned = (page.metadata.get("strategy") == "ocr_only" or 
                                 page.metadata.get("category") == "Image")
                    
                    page.metadata.update({
                        "course_code": course_code,
                        "university_source": filename,
                        "source_type": source_type,
                        "page_num": i + 1,
                        "topic": filename.replace(".pdf", ""),
                        "is_scanned": is_scanned
                    })
                all_docs.extend(pages)

    if not all_docs:
        print("❌ No documents found to index.")
        return None

    # --- 2. SEMANTIC CHUNKING ---
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(all_docs)

    # --- NEW: METADATA SANITIZATION ---
    # This removes the nested dictionaries (coordinates, points) that ChromaDB rejects
    chunks = filter_complex_metadata(chunks)
    print(f"🧹 Sanitized metadata for {len(chunks)} chunks.")

    # --- 3. DATABASE CLEANUP ---
    if os.path.exists(CHROMA_PATH):
        try:
            shutil.rmtree(CHROMA_PATH)
            print("🧹 Cleaned existing database.")
        except PermissionError:
            print("❌ Permission Denied: Close your main.py/terminal using the DB and try again.")
            return None

    # --- 4. MAXIMUM SPEED LOCAL UPLOAD ---
    # The RTX 3050 can handle massive batches instantly
    batch_size = 500 
    vector_db = None
    print(f"📦 Starting GPU-Accelerated Ingestion ({len(chunks)} chunks)...")

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        print(f"🚀 Uploading batch {i//batch_size + 1} of {(len(chunks)//batch_size)+1}...")
        
        if vector_db is None:
            vector_db = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=CHROMA_PATH
            )
        else:
            vector_db.add_documents(batch)
        
        # Notice: The 60-second time.sleep() has been completely deleted.

    print(f"✅ GPU Indexing Complete: {len(chunks)} chunks stored.")
    return vector_db

if __name__ == "__main__":
    build_vector_db()