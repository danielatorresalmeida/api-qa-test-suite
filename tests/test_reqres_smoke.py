import os
import pytest
from utils.api_client import APIClient


def test_users_list_ok():
    """Basic smoke test against ReqRes /users endpoint."""
    client = APIClient()
    if not client.headers.get("x-api-key"):
        if os.getenv("CI", "").lower() == "true":
            pytest.fail("REQRES_API_KEY is missing: CI must execute the live smoke test.")
        pytest.skip(
            "ReqRes requires x-api-key. Set REQRES_API_KEY locally to run this test."
        )

    resp = client.get("/users")
    assert resp.status_code == 200, (
        f"Expected 200 from {client.url('/users')}, got {resp.status_code}: {resp.text[:200]}"
    )
    body = resp.json()
    assert isinstance(body, dict)
    assert "data" in body

