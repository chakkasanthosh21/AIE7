"""Configuration settings for the Data Validation App."""

import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")
    
    # Guardrails Configuration
    guardrails_api_key: Optional[str] = Field(None, env="GUARDRAILS_API_KEY")
    
    # Vector Database Configuration
    vector_db_path: str = Field(default="./data/vector_db", env="VECTOR_DB_PATH")
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    
    # Application Configuration
    app_name: str = Field(default="AI Data Validation App", env="APP_NAME")
    debug: bool = Field(default=False, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # Validation Configuration
    max_file_size_mb: int = Field(default=100, env="MAX_FILE_SIZE_MB")
    supported_formats: list = Field(default=["csv", "json", "xlsx", "parquet"], env="SUPPORTED_FORMATS")
    
    # RAGAS Configuration
    ragas_metrics: list = Field(default=[
        "faithfulness", "answer_relevancy", "context_precision", 
        "context_recall", "answer_correctness"
    ])
    
    # LangGraph Configuration
    max_iterations: int = Field(default=10, env="MAX_ITERATIONS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
