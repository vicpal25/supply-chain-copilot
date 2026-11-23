"""Phase 1 task 3: write these tests first, then make them pass.

Tip: use httpx.MockTransport (or the respx library) to fake the server, so tests
never need a real model running.
"""

import pytest


@pytest.mark.skip(reason="Phase 1 task 3: implement OpenAICompatProvider")
async def test_complete_returns_text_and_usage(): ...


@pytest.mark.skip(reason="Phase 1 task 3: implement OpenAICompatProvider")
async def test_stream_yields_deltas_then_done(): ...
