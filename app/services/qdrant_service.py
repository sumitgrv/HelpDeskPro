from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from ..config import settings
from ..utils.logging import logger

_client = None

def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY or None)
    return _client

def ensure_collection(dim: int = 384):
    client = get_client()
    collections = client.get_collections().collections
    names = {c.name for c in collections}
    if settings.QDRANT_COLLECTION not in names:
        logger.info(f"Creating Qdrant collection {settings.QDRANT_COLLECTION}")
        client.recreate_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )

def upsert_points(points):
    client = get_client()
    client.upsert(collection_name=settings.QDRANT_COLLECTION, points=points)

def search(query_vector, top_k=5, filter=None):
    client = get_client()
    return client.search(collection_name=settings.QDRANT_COLLECTION, query_vector=query_vector, limit=top_k, query_filter=filter)
