import os

import pytest


def _require_api_key(api):
    """Ensure live tests only run when ReqRes is configured."""
    if api.headers.get("x-api-key"):
        return

    if os.getenv("CI", "").lower() == "true":
        pytest.fail(
            "REQRES_API_KEY is missing: CI must execute the live API tests."
        )

    pytest.skip(
        "ReqRes requires x-api-key. Set REQRES_API_KEY locally to run these tests."
    )


def _assert_user_shape(user):
    """Validate the essential fields returned for a ReqRes user."""
    assert isinstance(user, dict)

    required_fields = {
        "id",
        "email",
        "first_name",
        "last_name",
        "avatar",
    }

    assert required_fields.issubset(user.keys())
    assert isinstance(user["id"], int)
    assert isinstance(user["email"], str)
    assert "@" in user["email"]
    assert isinstance(user["first_name"], str)
    assert isinstance(user["last_name"], str)
    assert isinstance(user["avatar"], str)


def test_users_list_returns_valid_users(api):
    """GET /users should return a paginated list of users."""
    _require_api_key(api)

    response = api.get("/users", params={"page": 2})

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert body["page"] == 2
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0

    for user in body["data"]:
        _assert_user_shape(user)


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_existing_user_can_be_retrieved(api, user_id):
    """Known users should return HTTP 200 and the requested user id."""
    _require_api_key(api)

    response = api.get(f"/users/{user_id}")

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, dict)
    assert "data" in body

    user = body["data"]

    _assert_user_shape(user)
    assert user["id"] == user_id


def test_unknown_user_returns_404(api):
    """A user that does not exist should return HTTP 404."""
    _require_api_key(api)

    response = api.get("/users/23")

    assert response.status_code == 404