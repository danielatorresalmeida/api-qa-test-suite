import json
from pathlib import Path
import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="session")
def settings():
    """Load config once per session."""
    return json.loads(Path("config/settings.json").read_text())

@pytest.fixture(scope="session")
def api(settings):
    """Reusable API client for all tests."""
    return APIClient(base_url=settings["base_url"], token=settings.get("auth_token", ""))
