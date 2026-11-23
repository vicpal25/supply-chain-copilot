from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings, read from environment variables or a .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Which provider serves requests when the caller does not choose one.
    default_provider: Literal["anthropic", "openai_compat", "fake"] = "fake"

    # Anthropic (Claude). Set ANTHROPIC_API_KEY to enable.
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-5-5"

    # Any OpenAI-compatible server: Ollama, vLLM, LM Studio, etc.
    openai_compat_base_url: str = "http://localhost:11434/v1"
    openai_compat_model: str = "qwen2.5:3b"
    openai_compat_api_key: str = "not-needed"

    max_output_tokens: int = 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
