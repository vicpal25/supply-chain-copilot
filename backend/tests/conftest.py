import pytest
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app


@pytest.fixture
def client():
    app.dependency_overrides[get_settings] = lambda: Settings(
        _env_file=None, default_provider="fake", anthropic_api_key=None
    )
    yield TestClient(app)
    app.dependency_overrides.clear()
