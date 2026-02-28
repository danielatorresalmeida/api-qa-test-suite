import json
import os
from json import JSONDecodeError
from pathlib import Path
import requests

# Load config from config/settings.json (robust path + encoding)
ROOT = Path(__file__).resolve().parents[1]
_config_path = ROOT / "config" / "settings.json"
if not _config_path.exists():
    raise FileNotFoundError("Missing config/settings.json file")

def _load_config() -> dict:
    try:
        data = json.loads(_config_path.read_text(encoding="utf-8-sig"))
    except JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON in {_config_path}. Ensure valid JSON and UTF-8 encoding."
        ) from e

    # Optional profile via env var
    profile = os.getenv("API_PROFILE")
    if profile and isinstance(data, dict) and isinstance(data.get("profiles"), dict):
        prof = data["profiles"].get(profile)
        if isinstance(prof, dict):
            data = {**data, **prof}

    # Explicit env var overrides
    base = os.getenv("API_BASE_URL")
    if base:
        data["base_url"] = base
    token = os.getenv("API_AUTH_TOKEN")
    if token is not None and token != "":
        data["auth_token"] = token
    extra_headers = data.get("extra_headers")
    if not isinstance(extra_headers, dict):
        extra_headers = {}
    reqres_api_key = os.getenv("REQRES_API_KEY")
    if reqres_api_key:
        extra_headers["x-api-key"] = reqres_api_key
    data["extra_headers"] = extra_headers

    return data

config = _load_config()

class APIClient:
    def __init__(self, base_url=None, token=None):
        self.base_url = (base_url or config.get("base_url", "")).rstrip("/")
        tok = token or config.get("auth_token", "")
        self.headers = {
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {tok}"} if tok else {}),
        }
        # Allow additional headers from settings, e.g., x-api-key for ReqRes
        extras = config.get("extra_headers") or {}
        if isinstance(extras, dict):
            self.headers.update(extras)

    def url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint, params=None):
        return requests.get(self.url(endpoint), headers=self.headers, params=params, timeout=30)

    def post(self, endpoint, json=None):
        return requests.post(self.url(endpoint), headers=self.headers, json=json, timeout=30)

    def put(self, endpoint, json=None):
        return requests.put(self.url(endpoint), headers=self.headers, json=json, timeout=30)

    def patch(self, endpoint, json=None):
        return requests.patch(self.url(endpoint), headers=self.headers, json=json, timeout=30)

    def delete(self, endpoint):
        return requests.delete(self.url(endpoint), headers=self.headers, timeout=30)
