from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1)
    system: str | None = None
    provider: Literal["anthropic", "openai_compat", "fake"] | None = None
    max_tokens: int | None = Field(default=None, ge=1, le=8192)


class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0


class ChatResponse(BaseModel):
    provider: str
    model: str
    content: str
    usage: Usage
    latency_ms: float
