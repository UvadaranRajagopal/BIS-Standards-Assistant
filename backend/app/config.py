from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration"""

    # App info
    APP_NAME: str = "BIS Standards Assistant"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # RAG settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_PROVIDER: str = "llama3.2:3b"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 3

    # Database paths
    CHROMA_PERSIST_DIR: str = "./chroma_db"

    # Data residency
    DATA_RESIDENCY: str = "India"
    MODEL_VERSION: str = "v1.0.0"
    MODEL_TRAINED_ON: str = "2026-09-01"
    PDF_OUTPUT_DIR: str = "./pdf_output"


# Create a global settings instance
settings = Settings()