from collections.abc import AsyncIterator

from app.providers.base import Completion, StreamEvent
from app.schemas import Message, Usage


class FakeProvider:
    """Deterministic provider for tests and local UI work. Costs nothing, needs no key."""

    name = "fake"
    model = "fake-echo-1"

    def _reply(self, messages: list[Message]) -> str:
        return f"Echo: {messages[-1].content}"

    async def complete(
        self, messages: list[Message], system: str | None, max_tokens: int
    ) -> Completion:
        text = self._reply(messages)
        return Completion(
            content=text,
            model=self.model,
            usage=Usage(
                input_tokens=len(messages[-1].content.split()), output_tokens=len(text.split())
            ),
        )

    async def stream(
        self, messages: list[Message], system: str | None, max_tokens: int
    ) -> AsyncIterator[StreamEvent]:
        words = self._reply(messages).split(" ")
        for i, word in enumerate(words):
            yield StreamEvent(type="delta", text=word if i == 0 else f" {word}")
        yield StreamEvent(
            type="done",
            usage=Usage(input_tokens=len(messages[-1].content.split()), output_tokens=len(words)),
        )
