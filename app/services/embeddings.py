from sentence_transformers import SentenceTransformer
from .qdrant_service import ensure_collection
from ..config import settings
from ..utils.logging import logger

_model = None

def get_embedding_model():
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model

def embed_texts(texts):
    model = get_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True).tolist()
    return vectors
