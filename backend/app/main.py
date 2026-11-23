import json
import time
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.config import Settings, get_settings
from app.providers import LLMProvider, ProviderError, get_provider
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title="Supply Chain Copilot API", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


def resolve_provider(req: ChatRequest, settings: Settings) -> LLMProvider:
    try:
        return get_provider(req.provider or settings.default_provider, settings)
    except ProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, settings: SettingsDep) -> ChatResponse:
    provider = resolve_provider(req, settings)
    started = time.perf_counter()
    try:
        result = await provider.complete(
            req.messages, req.system, req.max_tokens or settings.max_output_tokens
        )
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    return ChatResponse(
        provider=provider.name,
        model=result.model,
        content=result.content,
        usage=result.usage,
        latency_ms=round((time.perf_counter() - started) * 1000, 2),
    )


def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@app.post("/v1/chat/stream")
async def chat_stream(req: ChatRequest, settings: SettingsDep):
    """Stream the reply as Server-Sent Events: `delta` events, then one `done` event.

    The `done` event carries token usage and time to first token, the first pieces of
    the telemetry you will build out in Phase 2.
    """
    provider = resolve_provider(req, settings)
    max_tokens = req.max_tokens or settings.max_output_tokens

    async def events() -> AsyncIterator[str]:
        started = time.perf_counter()
        first_token_ms: float | None = None
        try:
            async for ev in provider.stream(req.messages, req.system, max_tokens):
                if ev.type == "delta":
                    if first_token_ms is None:
                        first_token_ms = round((time.perf_counter() - started) * 1000, 2)
                    yield sse("delta", {"text": ev.text})
                elif ev.type == "done":
                    yield sse(
                        "done",
                        {
                            "provider": provider.name,
                            "usage": ev.usage.model_dump() if ev.usage else None,
                            "time_to_first_token_ms": first_token_ms,
                            "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                        },
                    )
        except Exception as exc:  # report errors in-band; headers are already sent
            yield sse("error", {"message": str(exc)})

    return StreamingResponse(events(), media_type="text/event-stream")
