import os
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_chroma import Chroma
# Ensure your config.py has both llm and refiner_llm defined
from config import llm, refiner_llm, embeddings, CHROMA_PATH

# --- 1. DEBUG UTILITIES ---

def debug_print_prompt(input_data):
    """Prints the formatted prompt before it hits the Generator LLM."""
    print("\n--- [DEBUG] GENERATOR PROMPT ---")
    print(input_data.to_string())
    print("----------------------------------\n")
    return input_data

def debug_retrieval(docs):
    """Prints which documents and pages were retrieved from the Vector DB."""
    print("\n--- [DEBUG] SEARCHING VECTOR DATABASE... ---")
    print(f"Found {len(docs)} relevant chunks.")
    return docs

# # --- 2. INITIALIZATION & HELPERS ---

vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

# UPGRADED: Using MMR to prevent repetitive chunk retrieval and expanding 'k' to 6
retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 6,               # Send 6 chunks to the LLM
        "fetch_k": 20,        # Pull 20 chunks from the DB first
        "lambda_mult": 0.7    # 70% Relevance / 30% Diversity
    }
)
def format_docs(docs):
    unique_contents = []
    seen = set()
    
    for doc in docs:
        # Extract metadata
        s_type = doc.metadata.get("source_type", "General")
        file = doc.metadata.get("university_source", "Unknown")
        page = doc.metadata.get("page_num", "?")
        
        # Warn the LLM when text comes from a scanned (OCR) source
        is_scanned = doc.metadata.get("is_scanned", False)
        scan_warning = "⚠️ SCANNED SOURCE (OCR) — text may contain character errors.\n" if is_scanned else ""
        enriched_content = f"[{s_type} SOURCE: {file}, Page {page}]\n{scan_warning}{doc.page_content.strip()}"
        
        if doc.page_content.strip() not in seen:
            unique_contents.append(enriched_content)
            seen.add(doc.page_content.strip())
            
    return "\n\n".join(unique_contents)

# --- 3. PROMPT TEMPLATES ---

# Phase 1: Contextualize the question
REFINEMENT_SYSTEM_PROMPT = """
You are a senior prompt engineer. Transform the student's question into an AI-optimized search query.
Output ONLY the refined, standalone question.
"""

rephrase_prompt = ChatPromptTemplate.from_messages([
    ("system", REFINEMENT_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# Phase 2: Grounded RAG Generation
system_prompt = """
You are an encouraging but grounded University Teaching Assistant. 
Your ONLY source of information is the 'COURSE CONCEPTS' provided below.

1. Use ONLY the provided concepts to answer.
2. If the student asks for exercises, rephrase "Examples" or "Tasks" from the concepts.
3. You may create fresh examples ONLY if they follow the exact logic (e.g. 0-based indexing) of the concepts.
4. If information is missing, state that you don't know based on the materials.

COURSE CONCEPTS:
{concept}
"""

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# Phase 3: Llama 4 Scout Polish
REFINER_SYSTEM_PROMPT = """
You are a senior pedagogical editor. You will receive a TA's draft response.
1. Polish the Markdown: Ensure code blocks and bolding are used for clarity.
2. Structure: Use bullet points to break up dense text.
3. Tone: Maintain an encouraging, clear, and academic tone.
4. Quality Control: Remove any repetitive phrases or glitchy text patterns.
5. OCR Repair: The source material may originate from scanned documents.
   Silently fix common OCR artifacts such as garbled variable names
   (e.g., 'vo1d' → 'void', 'pr1ntf' → 'printf', '0' ↔ 'O' confusion),
   corrupted mathematical symbols, and broken whitespace or line breaks.
6. Symbol Recovery: Restore standard programming and math notation
   where OCR has degraded it (e.g., '→' rendered as '->', '<=' as '⇐',
   curly braces eaten, subscripts flattened).
7. Guardrails: If the draft indicates that the information is missing or the query is irrelevant, refine it into a direct, polite refusal on behalf of the TA (e.g., "I'm sorry, but I don't have information on that topic in the course materials."). Do NOT mention being an editor, and do NOT ask for a draft response.
Output ONLY the polished response.
"""

refiner_prompt = ChatPromptTemplate.from_messages([
    ("system", REFINER_SYSTEM_PROMPT),
    ("human", "DRAFT RESPONSE: {original_response}")
])

# --- 4. THE MULTI-MODEL CHAIN ---

# Step A: The Rewriter
question_rewriter = rephrase_prompt | llm | StrOutputParser()

# Step B: The Generator Logic
rag_generator = (
    qa_prompt 
    | RunnableLambda(debug_print_prompt) 
    | llm 
    | StrOutputParser()
)

# Step C: The Refiner Chain
refiner_chain = refiner_prompt | refiner_llm | StrOutputParser()

# Step D: The Full Pipeline (MODIFIED TO RETAIN DOCUMENTS)
full_chain = (
    {
        "standalone_question": question_rewriter,
        "chat_history": itemgetter("chat_history"),
        "original_question": itemgetter("question")
    }
    # 1. Fetch and store the documents in the dictionary
    | RunnablePassthrough.assign(
        docs=itemgetter("standalone_question") | retriever | RunnableLambda(debug_retrieval)
    )
    # 2. Format the documents into a single text block for the LLM
    | RunnablePassthrough.assign(
        concept=itemgetter("docs") | RunnableLambda(format_docs)
    )
    # 3. Generate the draft response
    | RunnablePassthrough.assign(
        original_response=(
            {
                "concept": itemgetter("concept"),
                "question": itemgetter("original_question"),
                "chat_history": itemgetter("chat_history")
            }
            | rag_generator
        )
    )
    # 4. Refine the final response
    | RunnablePassthrough.assign(
        final_response=(
            {"original_response": itemgetter("original_response")}
            | refiner_chain
        )
    )
)

# --- 5. EXECUTION ---

chat_history = []

def ask_assistant(query):
    global chat_history
    print(f"\n--- 📥 Processing: '{query}' ---")
    
    # Run the full pipeline (returns a dictionary now, not just a string)
    result = full_chain.invoke({"question": query, "chat_history": chat_history})
    
    # Extract the pieces we want to show
    response = result["final_response"]
    retrieved_docs = result["docs"]
    
    # Update state for conversation memory
    from langchain_core.messages import HumanMessage, AIMessage
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response))
    
    # Keep the last 3 rounds of conversation to prevent token bloat
    if len(chat_history) > 8:
        chat_history = chat_history[-8:]
    
    # Print the TA's Answer
    print(f"\n🎓 TA Response:\n{response}")
    
    # --- NEW: PRINT CITED CHUNKS AT THE BOTTOM ---
    print("\n" + "=" * 50)
    print("📚 SOURCES USED FOR THIS ANSWER:")
    if not retrieved_docs:
        print("  - No context documents retrieved from database.")
    else:
        for i, doc in enumerate(retrieved_docs):
            source = doc.metadata.get("university_source", "Unknown Source")
            page = doc.metadata.get("page_num", "?")
            
            # Print the source file and page, plus a 100-character snippet of what the AI read
            print(f"\n[{i+1}] {source} (Page {page})")
            print(f"    Preview: \"{doc.page_content.strip()[:100]}...\"")
    print("=" * 50)
    
    return response, retrieved_docs


# --- 6. TERMINAL INTERFACE ---
if __name__ == "__main__":
    print("\n✅ uniguardian is online. Type 'exit' to shut down.")
    print("=" * 50)
    
    while True:
        user_input = input("\nStudent Prompt: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Shutting down uniguardian...")
            break
            
        ask_assistant(user_input)