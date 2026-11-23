# supply-chain-copilot

AI copilot for supply chain operations: streaming FastAPI backend, advanced RAG, multi-agent workflows, a secure MCP gateway, a fine-tuned small language model, and a compound AI router. Built with tracing and evals throughout.

This repo is a 24-week learning project. Each phase adds one layer to the same system.

| Phase | Weeks | Layer | Status |
| --- | --- | --- | --- |
| 1 | 1 to 3 | Headless AI backend: streaming API, provider abstraction, CI | In progress |
| 2 | 4 to 7 | Supplier knowledge RAG with tracing and evals | Not started |
| 3 | 8 to 11 | Multi-agent ops crew and streaming simulator UI | Not started |
| 4 | 12 to 15 | MCP gateway and security proxy | Not started |
| 5 | 16 to 20 | Fine-tuned, quantized small language model | Not started |
| 6 | 21 to 24 | Compound AI router and SDK | Not started |

## Quick start

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env          # add ANTHROPIC_API_KEY to use Claude
pytest                        # runs against the free fake provider
uvicorn app.main:app --reload
```

Try it:

```bash
curl -s localhost:8000/v1/chat -H 'content-type: application/json' \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'

curl -N localhost:8000/v1/chat/stream -H 'content-type: application/json' \
  -d '{"provider":"anthropic","messages":[{"role":"user","content":"List 3 causes of late shipments"}]}'
```

## Layout

```
backend/
  app/main.py              FastAPI app: /health, /v1/chat, /v1/chat/stream (SSE)
  app/providers/           One interface, many models: fake, anthropic, openai_compat
  tests/                   pytest suite (no API keys needed)
docs/phase-1.md            Your tasks for weeks 1 to 3
.github/workflows/ci.yml   Lint, test and Docker build on every PR
```
