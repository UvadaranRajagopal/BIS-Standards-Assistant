from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import audit, rag, standards, graph, pdf

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

# Allow React frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION
    }


@app.get("/")
async def root():
    return {
        "message": "Welcome to BIS Standards Assistant",
        "version": settings.VERSION,
        "data_residency": settings.DATA_RESIDENCY
    }


app.include_router(audit.router)
app.include_router(rag.router)
app.include_router(standards.router)
app.include_router(graph.router)
app.include_router(pdf.router)