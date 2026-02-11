from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_engine.app.api.ingest import embedder, rag
from ai_engine.app.services.llm_service import OllamaLLM

router = APIRouter()
llm = OllamaLLM(model="llama3.2:3b")

class Question(BaseModel):
    question: str

@router.post("/")
def ask(q: Question):
    # make sure a PDF was ingested
    if getattr(rag, "texts", None) is None or len(rag.texts) == 0:
        raise HTTPException(status_code=400, detail="No document ingested yet. Upload a PDF first.")

    q_emb = embedder.embed([q.question])[0]
    sources = rag.search(q_emb, k=4)

    context = "\n\n---\n\n".join(sources)

    prompt = f"""You are a helpful assistant.
Answer ONLY using the context below.
If the answer is not in the context, say: I don't know based on the document.

CONTEXT:
{context}

QUESTION:
{q.question}

ANSWER:
"""
    answer = llm.generate(prompt)

    return {"question": q.question, "answer": answer, "sources": sources}
