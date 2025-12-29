from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.payload import IngestPayload
from app.services.file_processing import FileProcessor
import os
from app.services.vector_store import VectorStore
from app.schemas.payload import SearchPayload, IngestPayload
from app.services.gemini_service import GeminiService
from app.schemas.payload import ChatPayload

router = APIRouter()

def run_ingestion_pipeline(repo_id: int, file_path: str):
    """
    The Worker Function: Runs in the background.
    1. Unzips and reads files.
    2. chunks and embeds them.
    """
    print(f"Starting pipeline for Repo {repo_id}...")

    processor = FileProcessor()

    try:
        # Process the File
        documents = processor.process_zip(file_path)
        
        # Chunk the text (Crucial Step!)
        # The AI can't read 10,000 lines at once. We split it.
        chunked_docs = []
        for doc in documents:
            chunks = processor.chunk_text(doc['text'])
            for chunk in chunks:
                meta = doc['metadata'].copy()
                meta['repo_id'] = repo_id  # add repo id tag to every chunk, so that faiss pull the code from the intended file
                chunked_docs.append({
                    "text": chunk,
                    "metadata": meta
                })
        # DEBUG PRINT
        if chunked_docs:
            print(f"Sample Metadata being sent to DB: {chunked_docs[0]['metadata']}")
        print(f"Split into {len(chunked_docs)} chunks. Embedding now...")

        # Embed and Store
        vector_db = VectorStore()
        vector_db.add_documents(chunked_docs)
        
        print(f"Repo {repo_id} successfully indexed!")

    except Exception as e:
        print(f"Pipeline failed for Repo {repo_id}: {e}")


@router.post("/ingest")
async def ingest_repository(payload: IngestPayload, background_tasks: BackgroundTasks):
    """
    The Entry Point:
    1. Validates input.
    2. Schedules the background task.
    3. Returns 'Accepted' immediately.
    """
    if not os.path.exists(payload.file_path):
        raise HTTPException(status_code=400, detail="File not found on server")

    # Add the function to the background queue
    background_tasks.add_task(run_ingestion_pipeline, payload.repo_id, payload.file_path)

    # send response back to the web_portal/signals.py as it can wait only for 5sec
    return {
        "status": "accepted", 
        "message": "Repository queued for ingestion",
        "repo_id": payload.repo_id
    }

@router.post("/search")
def search_repository(payload: SearchPayload):
    """
    Searches the Vector DB for code relevant to the query.
    """
    try:
        # Load the DB
        vector_db = VectorStore()
        # Run the search
        results = vector_db.search(payload.query, payload.repo_id, payload.limit)
        return {
            "query": payload.query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/chat")
def chat_with_repo(payload: ChatPayload):
    try:
        # The Retrieval (Get the relevant code)
        vector_db = VectorStore()
        # We fetch top 3 chunks to give the AI enough context
        search_results = vector_db.search(payload.query, payload.repo_id, k=3)
        
        # The Preparation (Combine chunks into one text block)
        if not search_results:
            return {"response": "I couldn't find any relevant code in this repository to answer your question."}
            
        context_text = "\n\n".join([res['text'] for res in search_results])
        
        # The Generation (Ask Gemini)
        # Note: Ideally, set GEMINI_API_KEY in your environment variables before running this
        gemini = GeminiService()
        ai_answer = gemini.generate_response(context_text, payload.query)
        
        return {
            "query": payload.query,
            "response": ai_answer,
            "context_used": [res['metadata']['source'] for res in search_results] # Optional: Show which files it read
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))