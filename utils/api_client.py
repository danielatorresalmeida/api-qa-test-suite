import json
from pathlib import Path
import requests

# Load config from config/settings.json
_config_path = Path("config/settings.json")
if not _config_path.exists():
    raise FileNotFoundError("Missing config/settings.json file")

config = json.loads(_config_path.read_text())

class APIClient:
    def __init__(self, base_url=None, token=None):
        self.base_url = (base_url or config.get("base_url", "")).rstrip("/")
        tok = token or config.get("auth_token", "")
        self.headers = {
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {tok}"} if tok else {}),
        }

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
