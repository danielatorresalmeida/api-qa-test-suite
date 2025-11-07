from utils.api_client import APIClient


def test_users_list_ok():
    """Basic smoke test against ReqRes /users endpoint."""
    client = APIClient()
    resp = client.get("/users")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict)
    assert "data" in body

