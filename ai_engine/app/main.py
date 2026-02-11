from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_engine.app.api.health import router as health_router
from ai_engine.app.api.ingest import router as ingest_router
from ai_engine.app.api.ask import router as ask_router

app = FastAPI(title="AI Engine", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health")
app.include_router(ingest_router, prefix="/ingest")
app.include_router(ask_router, prefix="/ask")
