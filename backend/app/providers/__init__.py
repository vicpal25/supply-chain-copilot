from app.config import Settings
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.base import LLMProvider, ProviderError
from app.providers.fake import FakeProvider
from app.providers.openai_compat import OpenAICompatProvider

__all__ = ["LLMProvider", "ProviderError", "get_provider"]


def get_provider(name: str, settings: Settings) -> LLMProvider:
    """Return the provider for `name`. Callers never import a vendor SDK directly."""
    if name == "fake":
        return FakeProvider()
    if name == "anthropic":
        return AnthropicProvider(settings)
    if name == "openai_compat":
        return OpenAICompatProvider(settings)
    raise ProviderError(f"Unknown provider: {name}")
