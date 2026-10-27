from qdrant_client import QdrantClient
from pydantic import BaseModel
from config import QDRANT_URL, QDRANT_API_KEY

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

class RAGInput(BaseModel):
    query: list   # 1536-dim embedding vector

def rag_search_tool(input_data: RAGInput):
    result = client.query_points(
        collection_name="moinsystems_knowledge",
        query=input_data.query,   # direct vector
        limit=3
    )

    docs = [point.payload.get("text", "") for point in result.points]
    return {"documents": docs}
