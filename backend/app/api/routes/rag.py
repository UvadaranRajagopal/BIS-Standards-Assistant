from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.retriever import retrieve_standards

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


@router.post("/search")
async def search(request: SearchRequest):
    """
    Search BIS standards using semantic similarity.
    """

    results = retrieve_standards(
        request.query,
        request.top_k
    )

    return {
        "query": request.query,
        "results": results
    }