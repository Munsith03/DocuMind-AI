from fastapi import APIRouter, UploadFile, File
from ai_engine.app.services.pdf_service import extract_text_from_pdf
from ai_engine.app.services.embedding_service import EmbeddingService
from ai_engine.app.services.rag_service import RAGService

router = APIRouter()

embedder = EmbeddingService()
rag = RAGService(dim=384)  # MiniLM embedding size

def chunk_text(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]

@router.post("/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    chunks = chunk_text(text)
    embeddings = embedder.embed(chunks)

    rag.add(embeddings, chunks)

    return {
        "message": "PDF ingested successfully",
        "chunks": len(chunks)
    }
