""" Centralized configuration for the application
Uses pydantic-settings for validated environment variables. """

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    openai_api_key: str
    anthropic_api_key: str
    primary_model: str = "gpt-4o-mini"
    fallback_model: str = "claude-haiku-4-5-20251001"
    pinecone_api_key: str
    pinecone_index_name: str = "personal-site-content"


    # LangSmith and LangChain settings
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "production-api"

    #Application settings
    app_env: str = "development"
    log_level: str = "INFO"
    rate_limit: str = "20/minute"
    cache_ttl_seconds: int = 300
    max_retries: int = 3

    # Comma-separated list of origins allowed to call this API.
    # Local dev defaults cover Live Server / VS Code. In production, set
    # ALLOWED_ORIGINS on Render to your real deployed frontend domain(s).
    allowed_origins: str = "http://127.0.0.1:5500,http://localhost:5500,http://localhost:5173,http://localhost:4173,,http://localhost:4175"

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
@lru_cache()
def get_settings() -> Settings:
    """Get the application settings, cached for performance."""
    return Settings()
