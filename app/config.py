import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    APP_ENV = os.getenv("APP_ENV", "dev")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./helpdeskpro.db")

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    RQ_QUEUE_NAME = os.getenv("RQ_QUEUE_NAME", "helpdeskpro")

    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "helpdesk_docs")

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "hf-fallback")  # openai|hf-fallback
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    FAKE_ENTERPRISE_SEARCH_URL = os.getenv("FAKE_ENTERPRISE_SEARCH_URL", "http://localhost:8000/fallback/search")

settings = Settings()
