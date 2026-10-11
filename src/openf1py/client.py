import httpx
from .exceptions import APIError
from .resources import DriversResource, SessionsResource, CarDataResource

class OpenF1Client:
    BASE_URL = "https://api.openf1.com/v1"

    def __init__(self, token: str | None = None, 
                 timeout: float = 30.0,
                 transport: httpx.BaseTransport | None = None):
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        self._http = httpx.Client(base_url=self.BASE_URL, headers=headers, timeout=timeout, transport=transport)
        self.drivers = DriversResource(self)
        self.sessions = SessionsResource(self)
        self.car_data = CarDataResource(self)

    def get(self, endpoint: str, **params) -> list[dict]:
        response = self._http.get(f"/{endpoint}", params=params)
        if response.is_error:
            raise APIError(response.status_code, response.text)
        return response.json()

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()