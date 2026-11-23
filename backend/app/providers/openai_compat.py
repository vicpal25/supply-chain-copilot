"""Provider for any OpenAI-compatible server (Ollama, vLLM, LM Studio).

YOUR TASK (Phase 1, week 2): implement this provider. See docs/phase-1.md, task 3.

Hints:
- POST {base_url}/chat/completions with {"model", "messages", "max_tokens", "stream"}.
- The system prompt goes in as the first message with role "system".
- With "stream": true the server sends Server-Sent Events: lines starting with "data: ",
  each a JSON chunk where choices[0].delta.content holds the text, ending with "data: [DONE]".
- Use httpx.AsyncClient and client.stream(...) / response.aiter_lines().
- Ask for usage with "stream_options": {"include_usage": true}; it arrives in the last chunk.
- Write the tests first: tests/test_openai_compat.py has a skipped test to start from.
"""

from collections.abc import AsyncIterator

from app.config import Settings
from app.providers.base import Completion, StreamEvent
from app.schemas import Message


class OpenAICompatProvider:
    name = "openai_compat"

    def __init__(self, settings: Settings) -> None:
        self.model = settings.openai_compat_model
        self.base_url = settings.openai_compat_base_url.rstrip("/")
        self.api_key = settings.openai_compat_api_key

    async def complete(
        self, messages: list[Message], system: str | None, max_tokens: int
    ) -> Completion:
        raise NotImplementedError("Phase 1 task 3: implement OpenAICompatProvider.complete")

    async def stream(
        self, messages: list[Message], system: str | None, max_tokens: int
    ) -> AsyncIterator[StreamEvent]:
        raise NotImplementedError("Phase 1 task 3: implement OpenAICompatProvider.stream")
        yield  # makes this an async generator
