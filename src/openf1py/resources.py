from __future__ import annotations
from typing import TYPE_CHECKING
from .model import Driver, Sessions, CarData

if TYPE_CHECKING:
    from .client import OpenF1Client

class DriversResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[Driver]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("drivers", **params)
        return [Driver.from_dict(d) for d in data]

class SessionsResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, year: int | None = None, country_name: str | None = None, session_name: str | None = None) -> list[Sessions]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "year": year,
            "country_name": country_name,
            "session_name": session_name,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("sessions", **params)
        return [Sessions.from_dict(d) for d in data]

class CarDataResource:
    def __init__(self, client: OpenF1Client):
        self._client = client

    def list(self, *, session_key: int | str | None = None, meeting_key: int | str | None = None, driver_number: int | None = None) -> list[CarData]:
        params = {
            "session_key": session_key,
            "meeting_key": meeting_key,
            "driver_number": driver_number,
        }

        # Don't send filter the user didn't set
        params = {k: v for k, v in params.items() if v is not None}

        data = self._client.get("car_data", **params)
        return [CarData.from_dict(d) for d in data]