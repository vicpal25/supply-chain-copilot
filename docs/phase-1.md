# Phase 1: Headless AI backend (weeks 1 to 3, about 8 hours a week)

**Goal:** one API that streams answers from Claude or an open model, tested and deployed to AWS through CI.

**Done when:** `/v1/chat/stream` works with both providers, CI is green, and the service runs on AWS.

Work test first: write or extend a failing test, make it pass, then refactor. Commit small.

## Week 1: understand the scaffold (reading about 2 hours, building about 6)

Read:
- FastAPI docs: async, dependencies, `StreamingResponse`
- MDN: Server-Sent Events
- Anthropic: "Building effective agents" and the Messages API streaming docs

Tasks:
- [ ] 1. Run the quick start. Read `app/main.py` and `app/providers/` until you can explain how a request reaches a model.
- [ ] 2. Get an Anthropic API key, add it to `.env`, and stream a real answer with `curl -N`. Note the `done` event: token usage and time to first token.

## Week 2: add a second provider

- [ ] 3. Implement `OpenAICompatProvider` (`app/providers/openai_compat.py`, hints are in the file).
  - Install [Ollama](https://ollama.com) and run `ollama pull qwen2.5:3b` to have a small local model.
  - Write the tests in `tests/test_openai_compat.py` first with `httpx.MockTransport`.
  - Remove the skip markers and the 501 test once it works.
- [ ] 4. Compare Claude and the small model on 5 supply chain prompts. Record latency, time to first token and token counts in `docs/notes/provider-comparison.md`. This is your first mini eval.

## Week 3: harden and deploy

- [ ] 5. Add timeouts and one retry with backoff for upstream calls. Test the failure path.
- [ ] 6. Add a request ID and structured JSON logs with provider, model, tokens and latency per request.
- [ ] 7. Deploy the Docker image to AWS (App Runner or ECS Fargate is simplest). Keep the API key in Secrets Manager, not in the image.
- [ ] 8. Extend CI to deploy on merge to `main` (GitHub OIDC to AWS, no long-lived keys).
- [ ] 9. Write a short ADR in `docs/adr/0001-provider-abstraction.md`: why one interface in front of every model, and what it costs.

## Stretch

- Add tool calling to the provider interface (needed for agents in Phase 3).
- Add a tiny Next.js page that renders the stream with the Vercel AI SDK.
