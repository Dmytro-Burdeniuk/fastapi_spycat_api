import requests
from typing import List, Any

from src.config import settings


class CatApiError(Exception):
    pass


class CatApiClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = base_url or settings.CAT_API_BASE_URL
        self.api_key = api_key or settings.CAT_API_KEY

    def search_breed(self, breed_name: str) -> List[dict[str, Any]]:
        url = f"{self.base_url}/breeds/search"
        headers: dict[str, str] = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        try:
            resp = requests.get(
                url,
                params={"q": breed_name},
                headers=headers,
                timeout=5,
            )
        except requests.RequestException as exc:
            raise CatApiError("Error contacting TheCatAPI") from exc

        if resp.status_code != 200:
            raise CatApiError("TheCatAPI returned an error")

        breeds = resp.json()

        if not breeds:
            raise CatApiError(f"No such breed: {breed_name!r}")

        return breeds
