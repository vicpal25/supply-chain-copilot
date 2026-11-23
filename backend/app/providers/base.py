from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Protocol

from app.schemas import Message, Usage


class ProviderError(Exception):
    """Raised when a provider is misconfigured or the upstream call fails."""


@dataclass
class Completion:
    content: str
    model: str
    usage: Usage = field(default_factory=Usage)


@dataclass
class StreamEvent:
    """One event in a streamed response.

    type is "delta" for a text chunk, or "done" once at the end with usage filled in.
    """

    type: str
    text: str = ""
    usage: Usage | None = None


class LLMProvider(Protocol):
    name: str

    async def complete(
        self, messages: list[Message], system: str | None, max_tokens: int
    ) -> Completion: ...

    def stream(
        self, messages: list[Message], system: str | None, max_tokens: int
    ) -> AsyncIterator[StreamEvent]: ...
