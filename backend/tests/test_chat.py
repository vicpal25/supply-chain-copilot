def test_chat_uses_default_provider(client):
    resp = client.post(
        "/v1/chat", json={"messages": [{"role": "user", "content": "where is PO 42"}]}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["provider"] == "fake"
    assert body["content"] == "Echo: where is PO 42"
    assert body["usage"]["output_tokens"] > 0
    assert body["latency_ms"] >= 0


def test_chat_rejects_empty_messages(client):
    resp = client.post("/v1/chat", json={"messages": []})
    assert resp.status_code == 422


def test_anthropic_without_key_is_a_clear_400(client):
    resp = client.post(
        "/v1/chat",
        json={"provider": "anthropic", "messages": [{"role": "user", "content": "hi"}]},
    )
    assert resp.status_code == 400
    assert "ANTHROPIC_API_KEY" in resp.json()["detail"]


def test_unimplemented_provider_returns_501(client):
    resp = client.post(
        "/v1/chat",
        json={"provider": "openai_compat", "messages": [{"role": "user", "content": "hi"}]},
    )
    assert resp.status_code == 501
