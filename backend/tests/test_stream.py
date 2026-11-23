import json


def parse_sse(raw: str) -> list[tuple[str, dict]]:
    events = []
    for block in raw.strip().split("\n\n"):
        lines = dict(line.split(": ", 1) for line in block.splitlines())
        events.append((lines["event"], json.loads(lines["data"])))
    return events


def test_stream_sends_deltas_then_done(client):
    with client.stream(
        "POST",
        "/v1/chat/stream",
        json={"messages": [{"role": "user", "content": "late shipments"}]},
    ) as resp:
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/event-stream")
        events = parse_sse(resp.read().decode())

    kinds = [kind for kind, _ in events]
    assert kinds[-1] == "done"
    assert set(kinds[:-1]) == {"delta"}
    assert (
        "".join(data["text"] for kind, data in events if kind == "delta") == "Echo: late shipments"
    )

    done = events[-1][1]
    assert done["provider"] == "fake"
    assert done["usage"]["output_tokens"] == 3
    assert done["time_to_first_token_ms"] is not None
