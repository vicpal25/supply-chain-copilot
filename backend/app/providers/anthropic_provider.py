from collections.abc import AsyncIterator

from anthropic import AsyncAnthropic

from app.config import Settings
from app.providers.base import Completion, ProviderError, StreamEvent
from app.schemas import Message, Usage


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, settings: Settings) -> None:
        if not settings.anthropic_api_key:
            raise ProviderError("ANTHROPIC_API_KEY is not set")
        self.model = settings.anthropic_model
        self._client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    def _params(self, messages: list[Message], system: str | None, max_tokens: int) -> dict:
        params: dict = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [m.model_dump() for m in messages],
        }
        if system:
            params["system"] = system
        return params

    async def complete(
        self, messages: list[Message], system: str | None, max_tokens: int
    ) -> Completion:
        resp = await self._client.messages.create(**self._params(messages, system, max_tokens))
        text = "".join(block.text for block in resp.content if block.type == "text")
        return Completion(
            content=text,
            model=resp.model,
            usage=Usage(
                input_tokens=resp.usage.input_tokens, output_tokens=resp.usage.output_tokens
            ),
        )

    async def stream(
        self, messages: list[Message], system: str | None, max_tokens: int
    ) -> AsyncIterator[StreamEvent]:
        async with self._client.messages.stream(
            **self._params(messages, system, max_tokens)
        ) as stream:
            async for text in stream.text_stream:
                yield StreamEvent(type="delta", text=text)
            final = await stream.get_final_message()
        yield StreamEvent(
            type="done",
            usage=Usage(
                input_tokens=final.usage.input_tokens, output_tokens=final.usage.output_tokens
            ),
        )
