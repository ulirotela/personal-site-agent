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

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"
@lru_cache()
def get_settings() -> Settings:
    """Get the application settings, cached for performance."""
    return Settings()
